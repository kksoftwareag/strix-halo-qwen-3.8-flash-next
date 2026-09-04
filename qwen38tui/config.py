"""Server-Konfiguration: Datenmodell, Validierung und Übersetzung in `llama serve`-Argumente + Umgebung."""
from __future__ import annotations

import json
import shlex
from dataclasses import dataclass, field, asdict, fields
from pathlib import Path
from typing import Any

from .discovery import Inventory, Engine, ModelFile, MtpHead, STATE_DIR
from .hardware import HardwareInfo

KV_TYPES = ["f16", "q8_0", "bf16", "f32", "q4_0", "q4_1", "iq4_nl", "q5_0", "q5_1"]
REASONING_EFFORTS = ["xhigh", "medium", "low"]           # laut Chat-Template des Modells (Default xhigh)
LOAD_MODES = ["mmap", "mmap+mlock", "mlock", "none", "auto"]
LAZY_MODES = ["auto", "on", "off"]
TRISTATE = ["auto", "on", "off"]
CTX_CHOICES = [8192, 16384, 32768, 65536, 98304, 131072, 196608, 262144]
UBATCH_CHOICES = [256, 512, 1024, 2048]
BATCH_CHOICES = [512, 1024, 2048, 4096]


@dataclass
class ServerConfig:
    # --- Engine / Modell ---
    engine: str = "auto"                 # Engine-Key aus discovery, "auto" = bester HIP-Build mit MTP
    quant: str = "auto"                  # Quant-Name, "auto" = bester Quant, der ins Speicherbudget passt
    tensor_read_lazy: str = "auto"       # auto|on|off  (PLE-Tabelle 26.8 GiB lazy von Platte lesen)
    no_host: bool = False                # --no-host: keine gepinnten Host-Puffer (nur mit mmap relevant)
    ple_cpu_override: bool = False       # -ot per_layer_token_embd.weight=CPU (Alternative zu --no-host, nur dieser Tensor)
    load_mode: str = "auto"              # auto (ROCm: kein mmap, schneller Upload) | mmap (lazy PLE, aber Upload ~18 MB/s!) | mlock | none
    n_gpu_layers: int = 99
    # --- Kontext / KV-Cache / Batching ---
    ctx_size: int = 131072
    cache_type_k: str = "q8_0"
    cache_type_v: str = "q8_0"
    flash_attn: str = "on"               # on|off|auto
    batch_size: int = 2048
    ubatch_size: int = 512
    threads: int = 16
    threads_batch: int = 0               # 0 = wie threads
    n_parallel: int = 1
    kv_unified: str = "auto"             # auto|on|off
    cache_ram_mib: int = 8192            # Prompt-Cache im RAM (MiB); -1 unbegrenzt, 0 aus
    cache_reuse: int = 0
    # --- Spekulatives Decoding (MTP) ---
    mtp_enabled: bool = True
    mtp_head: str = "auto"
    spec_draft_n_max: int = 3
    spec_draft_n_min: int = 0
    spec_draft_p_min: float = 0.75
    spec_draft_p_split: float = 0.10
    spec_extra_types: str = ""           # z.B. "ngram-mod" -> --spec-type draft-mtp,ngram-mod
    # --- Reasoning ---
    thinking: bool = True
    reasoning_effort: str = "medium"     # xhigh|medium|low
    reasoning_budget: int = -1
    reasoning_format: str = "auto"       # auto|none|deepseek|deepseek-legacy
    # --- Sampling-Defaults (vom Client überschreibbar) ---
    temp: float = 1.0
    top_p: float = 0.95
    top_k: int = 20
    min_p: float = 0.0
    presence_penalty: float = 0.0
    repeat_penalty: float = 1.0
    # --- Server ---
    host: str = "auto"                   # auto = primäre IP (LAN), sonst z.B. 127.0.0.1 / 0.0.0.0
    port: int = 8080
    api_key: str = ""
    alias: str = "qwen3.8-flash"
    metrics: bool = True
    webui: bool = True
    warmup: bool = True
    sleep_idle_seconds: int = -1
    timeout: int = 3600
    log_verbosity: int = 4               # -lv: 4 zeigt Puffergrößen/lazy-Meldungen von libllama im Log
    # --- Umgebung / Extras ---
    attn_rot_disable: str = "off"        # off = Hadamard-Rotation aktiv (bessere Qualität bei quantisiertem KV, gemessen ~2 % tg); on = Env setzen; auto = wie off (Load ohne Env verifiziert)
    extra_args: str = ""
    extra_env: dict[str, str] = field(default_factory=dict)
    profile_name: str = "standard"
    hipblaslt: bool = False              # ROCBLAS_USE_HIPBLASLT=1 (EngramHalo-Empfehlung; messen)
    # --- TUI-Schutz (nicht Teil der Kommandozeile) ---
    mem_guard_gib: float = 6.0           # Server hart stoppen, wenn MemAvailable darunter fällt (0 = aus)

    # ------------------------------------------------------------------ Persistenz
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "ServerConfig":
        known = {f.name for f in fields(cls)}
        clean = {k: v for k, v in d.items() if k in known}
        cfg = cls(**clean)
        cfg.normalize()
        return cfg

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False))

    @classmethod
    def load(cls, path: Path) -> "ServerConfig":
        return cls.from_dict(json.loads(path.read_text()))

    def copy(self, **overrides: Any) -> "ServerConfig":
        d = self.to_dict()
        d.update(overrides)
        return ServerConfig.from_dict(d)

    def normalize(self) -> None:
        """Typen und Wertebereiche geraderücken (nach Laden aus JSON / Eingabefeldern)."""
        self.ctx_size = max(512, int(self.ctx_size))
        self.batch_size = max(32, int(self.batch_size))
        self.ubatch_size = max(32, min(int(self.ubatch_size), self.batch_size))
        self.threads = max(1, int(self.threads))
        self.threads_batch = max(0, int(self.threads_batch))
        self.n_parallel = max(1, int(self.n_parallel))
        self.spec_draft_n_max = max(1, min(int(self.spec_draft_n_max), 16))
        self.spec_draft_n_min = max(0, min(int(self.spec_draft_n_min), self.spec_draft_n_max))
        self.spec_draft_p_min = min(max(float(self.spec_draft_p_min), 0.0), 1.0)
        self.spec_draft_p_split = min(max(float(self.spec_draft_p_split), 0.0), 1.0)
        self.temp = max(0.0, float(self.temp))
        self.top_p = min(max(float(self.top_p), 0.0), 1.0)
        self.top_k = max(0, int(self.top_k))
        self.min_p = min(max(float(self.min_p), 0.0), 1.0)
        self.port = min(max(int(self.port), 1), 65535)
        if self.reasoning_effort not in REASONING_EFFORTS:
            self.reasoning_effort = "medium"
        if self.cache_type_k not in KV_TYPES:
            self.cache_type_k = "f16"
        if self.cache_type_v not in KV_TYPES:
            self.cache_type_v = "f16"

    # ------------------------------------------------------------------ Ableitungen
    @property
    def kv_quantized(self) -> bool:
        return self.cache_type_k not in ("f16", "bf16", "f32") or self.cache_type_v not in ("f16", "bf16", "f32")

    def chat_template_kwargs(self) -> dict[str, Any]:
        kw: dict[str, Any] = {}
        if self.thinking:
            kw["reasoning_effort"] = self.reasoning_effort
        else:
            kw["enable_thinking"] = False
        return kw

    def spec_types(self) -> list[str]:
        types = ["draft-mtp"] if self.mtp_enabled else []
        for t in (x.strip() for x in self.spec_extra_types.split(",")):
            if t and t not in types:
                types.append(t)
        return types


@dataclass
class Resolved:
    engine: Engine | None
    model: ModelFile | None
    mtp: MtpHead | None
    host: str


@dataclass
class Command:
    argv: list[str]
    env: dict[str, str]
    resolved: Resolved
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def shell(self) -> str:
        env = " ".join(f"{k}={shlex.quote(v)}" for k, v in self.env.items())
        return (env + " " if env else "") + " ".join(shlex.quote(a) for a in self.argv)

    def pretty(self) -> str:
        """Mehrzeilige Darstellung für die Vorschau."""
        lines = [f"export {k}={shlex.quote(v)}" for k, v in self.env.items()]
        args = self.argv
        out = [shlex.quote(args[0])]
        i = 1
        while i < len(args):
            a = args[i]
            if a.startswith("-") and i + 1 < len(args) and not args[i + 1].startswith("-"):
                out.append(f"  {a} {shlex.quote(args[i + 1])}")
                i += 2
            else:
                out.append(f"  {a}")
                i += 1
        lines.append(" \\\n".join(out))
        return "\n".join(lines)


def resolve(cfg: ServerConfig, inv: Inventory, hw: HardwareInfo | None, fits: "callable | None" = None) -> Resolved:
    """Engine, Modell, MTP-Head und Host konkret auflösen."""
    engine = inv.engine(cfg.engine) if cfg.engine != "auto" else inv.default_engine(prefer_mtp=cfg.mtp_enabled)
    model: ModelFile | None = None
    if cfg.quant != "auto":
        model = inv.model(cfg.quant)
    else:
        # bester Quant, der passt (Liste ist qualitativ aufsteigend sortiert)
        for m in reversed(inv.models):
            if fits is None or fits(m):
                model = m
                break
        if model is None and inv.models:
            model = inv.models[0]
    mtp: MtpHead | None = None
    if cfg.mtp_enabled and inv.mtp_heads:
        mtp = inv.mtp(cfg.mtp_head) if cfg.mtp_head != "auto" else None
        if mtp is None:
            # auto: erster Head, dessen Tensor-Namen zum Loader der Engine passen (dzannotti-Design für die lokalen Forks)
            mtp = next((h for h in inv.mtp_heads if h.compatible_with(engine)), None)
    host = cfg.host
    if host == "auto":
        host = hw.primary_ip if hw and hw.primary_ip else "127.0.0.1"
    return Resolved(engine, model, mtp, host)


def build_command(cfg: ServerConfig, inv: Inventory, hw: HardwareInfo | None, fits: "callable | None" = None) -> Command:
    r = resolve(cfg, inv, hw, fits)
    errors: list[str] = []
    warnings: list[str] = []
    env: dict[str, str] = {}
    if r.engine is None:
        errors.append("Kein llama.cpp-Build gefunden – engine/fetch.sh und engine/build-engramhalo.sh bzw. engine/build.sh hip ausführen (oder QWEN38_ENGINES setzen).")
    if r.model is None:
        errors.append("Kein Qwen3.8-Flash-Next-GGUF gefunden – z.B. `hf download unsloth/Qwen3.8-Flash-Next-GGUF --include 'UD-Q4_K_XL/*'` oder QWEN38_MODEL_DIRS setzen.")
    if errors:
        return Command([], env, r, errors, warnings)
    assert r.engine and r.model

    argv = r.engine.serve_argv()
    argv += ["-m", str(r.model.path)]
    argv += ["-ngl", str(cfg.n_gpu_layers)]
    argv += ["-c", str(cfg.ctx_size)]
    argv += ["-fa", cfg.flash_attn]
    argv += ["-ctk", cfg.cache_type_k, "-ctv", cfg.cache_type_v]
    argv += ["-b", str(cfg.batch_size), "-ub", str(cfg.ubatch_size)]
    argv += ["-t", str(cfg.threads)]
    if cfg.threads_batch:
        argv += ["-tb", str(cfg.threads_batch)]
    if cfg.tensor_read_lazy != "auto":
        # EngramHalo (älterer Flag-Name): --lazy-mode; Stock-Fork: --tensor-read-lazy
        argv += ["--lazy-mode" if r.engine.fast_lazy_ple else "--tensor-read-lazy", cfg.tensor_read_lazy]
    if cfg.no_host:
        argv += ["--no-host"]
    if cfg.ple_cpu_override:
        argv += ["-ot", "per_layer_token_embd.weight=CPU"]
    if cfg.load_mode != "auto":
        argv += ["--load-mode", cfg.load_mode]
    argv += ["-np", str(cfg.n_parallel)]
    if cfg.kv_unified == "on":
        argv += ["--kv-unified"]
    elif cfg.kv_unified == "off":
        argv += ["--no-kv-unified"]
    argv += ["--cache-ram", str(cfg.cache_ram_mib)]
    if cfg.cache_reuse:
        argv += ["--cache-reuse", str(cfg.cache_reuse)]

    # Spekulatives Decoding
    if cfg.mtp_enabled:
        if not r.engine.supports_mtp:
            warnings.append(f"Engine '{r.engine.key}' hat keinen qwen4exp-MTP-Patch – MTP wird ausgelassen.")
        elif r.mtp is None:
            warnings.append("Kein zur Engine passender MTP-Draft-Head gefunden – MTP wird ausgelassen.")
        elif not r.mtp.compatible_with(r.engine):
            errors.append(f"MTP-Head „{r.mtp.path.name}“ nutzt {r.mtp.style}-Tensornamen, die Engine erwartet {r.engine.mtp_head_style} – Laden würde abbrechen.")
        else:
            argv += ["-md", str(r.mtp.path), "-ngld", "99"]
            argv += ["--spec-type", ",".join(cfg.spec_types())]
            argv += ["--spec-draft-n-max", str(cfg.spec_draft_n_max)]
            if cfg.spec_draft_n_min:
                argv += ["--spec-draft-n-min", str(cfg.spec_draft_n_min)]
            argv += ["--spec-draft-p-min", f"{cfg.spec_draft_p_min:g}"]
            if abs(cfg.spec_draft_p_split - 0.10) > 1e-9:
                argv += ["--spec-draft-p-split", f"{cfg.spec_draft_p_split:g}"]
            if cfg.spec_draft_n_max > 4:
                warnings.append("MTP-Head hat 1 Draft-Layer; auf bandbreitenlimitierter Hardware gewinnen kleine Tiefen (2–4) – n_max > 4 per Benchmark prüfen.")
    elif cfg.spec_extra_types.strip():
        argv += ["--spec-type", ",".join(cfg.spec_types())]

    # Reasoning / Template
    argv += ["--jinja"]
    argv += ["--chat-template-kwargs", json.dumps(cfg.chat_template_kwargs())]
    if cfg.reasoning_budget >= 0:
        argv += ["--reasoning-budget", str(cfg.reasoning_budget)]
    if cfg.reasoning_format != "auto":
        argv += ["--reasoning-format", cfg.reasoning_format]

    # Sampling
    argv += ["--temp", f"{cfg.temp:g}", "--top-p", f"{cfg.top_p:g}", "--top-k", str(cfg.top_k), "--min-p", f"{cfg.min_p:g}"]
    if cfg.presence_penalty:
        argv += ["--presence-penalty", f"{cfg.presence_penalty:g}"]
    if abs(cfg.repeat_penalty - 1.0) > 1e-9:
        argv += ["--repeat-penalty", f"{cfg.repeat_penalty:g}"]

    # Server
    argv += ["--host", r.host, "--port", str(cfg.port)]
    if cfg.alias:
        argv += ["-a", cfg.alias]
    if cfg.api_key:
        argv += ["--api-key", cfg.api_key]
    if cfg.metrics:
        argv += ["--metrics"]
    if not cfg.webui:
        argv += ["--no-webui"]
    if not cfg.warmup:
        argv += ["--no-warmup"]
    if cfg.sleep_idle_seconds > 0:      # 0 wird vom Server abgelehnt (-1 = aus)
        argv += ["--sleep-idle-seconds", str(cfg.sleep_idle_seconds)]
    if cfg.timeout != 3600:
        argv += ["-to", str(cfg.timeout)]
    if cfg.log_verbosity >= 0:
        argv += ["-lv", str(cfg.log_verbosity)]
    if cfg.extra_args.strip():
        try:
            argv += shlex.split(cfg.extra_args)
        except ValueError as e:
            errors.append(f"Zusätzliche Argumente nicht parsebar: {e}")

    # Umgebung
    rot = cfg.attn_rot_disable
    if rot == "auto":
        rot = "off"   # b10685 + Patch laden quantisierten KV mit aktiver Rotation (gemessen 2026-09-03)
    if rot == "on":
        env["LLAMA_ATTN_ROT_DISABLE"] = "1"
    if cfg.hipblaslt:
        env["ROCBLAS_USE_HIPBLASLT"] = "1"
    env.update({k: str(v) for k, v in cfg.extra_env.items() if k})

    # Plausibilitäten
    ctx_train = int(r.model.meta.get("qwen4exp.context_length", 262144) or 262144)
    if cfg.ctx_size > ctx_train:
        warnings.append(f"Kontext {cfg.ctx_size} > Trainingskontext {ctx_train} (RoPE-Skalierung nötig, Qualität sinkt).")
    if r.engine.backend == "hip" and cfg.load_mode in ("mmap", "mmap+mlock") and not r.engine.fast_lazy_ple:
        warnings.append("--load-mode mmap auf ROCm (Stock-Fork): Gewichte-Upload läuft seitenweise (~18 MB/s gemessen, Page-Cache-Thrash) – Ladezeit >2 h bei Q4_K_XL. Nur EngramHalo macht SSD-lazy praktikabel.")
    elif cfg.load_mode not in ("mmap", "mmap+mlock") and cfg.tensor_read_lazy != "off" and r.model.ple_bytes and not r.engine.fast_lazy_ple:
        warnings.append("Ohne mmap liegt die PLE-Tabelle (26.8 GiB) komplett im RAM (in der Speicherbilanz berücksichtigt). EngramHalo-Engine hält sie in jedem Lade-Modus lazy (~2.6 GiB).")
    if cfg.kv_quantized and cfg.flash_attn == "off":
        warnings.append("Quantisierter V-Cache erfordert Flash Attention (-fa on).")
    if cfg.kv_quantized and rot == "on":
        warnings.append("LLAMA_ATTN_ROT_DISABLE=1 schaltet die Hadamard-Rotation ab: schneller (~2 %), aber schlechtere Qualität des quantisierten KV-Caches (PR #21038).")
    if cfg.thinking and cfg.reasoning_effort not in REASONING_EFFORTS:
        errors.append("reasoning_effort muss xhigh, medium oder low sein (Chat-Template wirft sonst eine Exception).")
    if cfg.ubatch_size > cfg.batch_size:
        errors.append("ubatch darf nicht größer als batch sein.")
    if cfg.n_parallel > 1 and cfg.mtp_enabled:
        warnings.append("MTP bei mehreren Slots kostet Durchsatz (gemessen: 8 Nutzer 35 t/s mit MTP vs 50 t/s ohne) – für Mehrnutzer MTP aus, für Einzelnutzer an.")
    if hw and cfg.threads > hw.cores_physical > 0:
        warnings.append(f"threads={cfg.threads} > physische Kerne ({hw.cores_physical}); SMT bringt bei llama.cpp meist nichts.")
    if r.host not in ("127.0.0.1", "localhost") and not cfg.api_key:
        warnings.append(f"Server lauscht auf {r.host} ohne API-Key (nur in vertrauenswürdigem LAN).")
    return Command(argv, env, r, errors, warnings)


# ------------------------------------------------------------------ Profile
PROFILES_DIR = STATE_DIR / "profiles"
CURRENT_CONFIG = STATE_DIR / "current.json"


def list_profiles() -> list[str]:
    if not PROFILES_DIR.is_dir():
        return []
    return sorted(p.stem for p in PROFILES_DIR.glob("*.json"))


def save_profile(cfg: ServerConfig, name: str) -> Path:
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in name.strip()) or "profil"
    cfg.profile_name = safe
    p = PROFILES_DIR / f"{safe}.json"
    cfg.save(p)
    return p


def load_profile(name: str) -> ServerConfig:
    return ServerConfig.load(PROFILES_DIR / f"{name}.json")


def delete_profile(name: str) -> None:
    p = PROFILES_DIR / f"{name}.json"
    if p.exists():
        p.unlink()
