"""Hardware- und Systemzustand: RAM, GPU-Speicher (VRAM/GTT), CPU, Governor, tuned, Kernel-Parameter, Störprozesse."""
from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

GIB = 2**30


def _read(path: str | Path, default: str = "") -> str:
    try:
        return Path(path).read_text().strip()
    except OSError:
        return default


def _run(argv: list[str], timeout: float = 5) -> str:
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=timeout).stdout
    except Exception:
        return ""


@dataclass
class Tip:
    level: str      # "ok" | "hinweis" | "warnung"
    topic: str
    text: str
    command: str = ""


@dataclass
class HardwareInfo:
    cpu_model: str = "?"
    cores_physical: int = 0
    threads_logical: int = 0
    mem_total: int = 0
    mem_available: int = 0
    mem_cached: int = 0
    swap_total: int = 0
    gpu_name: str = "?"
    vram_total: int = 0
    vram_used: int = 0
    gtt_total: int = 0
    gtt_used: int = 0
    gfx_target: str = ""
    rocm_version: str = ""
    kernel: str = ""
    cmdline: str = ""
    governor: str = ""
    epp: str = ""
    tuned_profile: str = ""
    ppd_profile: str = ""
    platform_profile: str = ""
    thp: str = ""
    gpu_perf_level: str = ""
    primary_ip: str = ""
    hostname: str = ""
    other_llm_procs: list[dict[str, Any]] = field(default_factory=list)
    tips: list[Tip] = field(default_factory=list)

    @property
    def usable_for_model(self) -> int:
        """Konservatives Budget für Modell+KV+Compute: MemAvailable minus Reserve für OS/Page-Cache."""
        return max(0, self.mem_available - 6 * GIB)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _meminfo() -> dict[str, int]:
    out: dict[str, int] = {}
    for line in _read("/proc/meminfo").splitlines():
        m = re.match(r"(\w+):\s+(\d+)\s*kB", line)
        if m:
            out[m.group(1)] = int(m.group(2)) * 1024
    return out


def _cpu() -> tuple[str, int, int]:
    model, phys, logical = "?", 0, os.cpu_count() or 0
    txt = _read("/proc/cpuinfo")
    m = re.search(r"model name\s*:\s*(.+)", txt)
    if m:
        model = m.group(1).strip()
    cores = set()
    for block in txt.split("\n\n"):
        pid = re.search(r"physical id\s*:\s*(\d+)", block)
        cid = re.search(r"core id\s*:\s*(\d+)", block)
        if pid and cid:
            cores.add((pid.group(1), cid.group(1)))
    phys = len(cores) or logical
    return model, phys, logical


def _gpu() -> dict[str, Any]:
    d: dict[str, Any] = {"name": "?", "vram_total": 0, "vram_used": 0, "gtt_total": 0, "gtt_used": 0, "gfx": "", "perf_level": ""}
    for card in sorted(Path("/sys/class/drm").glob("card[0-9]")):
        dev = card / "device"
        if not (dev / "mem_info_vram_total").exists():
            continue
        d["vram_total"] = int(_read(dev / "mem_info_vram_total", "0") or 0)
        d["vram_used"] = int(_read(dev / "mem_info_vram_used", "0") or 0)
        d["gtt_total"] = int(_read(dev / "mem_info_gtt_total", "0") or 0)
        d["gtt_used"] = int(_read(dev / "mem_info_gtt_used", "0") or 0)
        d["perf_level"] = _read(dev / "power_dpm_force_performance_level")
        break
    lspci = _run(["lspci"])
    m = re.search(r"(?:VGA|Display|3D).*?:\s*(.+)", lspci)
    if m:
        d["name"] = m.group(1).strip()
    if shutil.which("rocminfo"):
        ri = _run(["rocminfo"], timeout=10)
        g = re.search(r"Name:\s+(gfx\d+\w*)", ri)
        if g:
            d["gfx"] = g.group(1)
        mk = re.search(r"Marketing Name:\s+(AMD Radeon[^\n]+)", ri)
        if mk:
            d["name"] = mk.group(1).strip()
    return d


def _rocm_version() -> str:
    for p in ("/opt/rocm/.info/version", "/usr/share/doc/rocm-core/version"):
        v = _read(p)
        if v:
            return v
    out = _run(["hipcc", "--version"], timeout=10)
    m = re.search(r"HIP version:\s*([\d.]+)", out)
    return m.group(1) if m else ""


def _primary_ip() -> str:
    out = _run(["ip", "-4", "route", "get", "1.1.1.1"])
    m = re.search(r"src\s+(\d+\.\d+\.\d+\.\d+)", out)
    return m.group(1) if m else "127.0.0.1"


def _other_llm_procs() -> list[dict[str, Any]]:
    procs: list[dict[str, Any]] = []
    out = _run(["ps", "-eo", "pid,rss,comm,args", "--sort=-rss"])
    for line in out.splitlines()[1:]:
        parts = line.split(None, 3)
        if len(parts) < 4:
            continue
        pid, rss, comm, args = parts
        if re.search(r"llama|ollama|vllm|lmstudio|lms\b|koboldcpp|text-generation", comm + " " + args, re.I):
            if "qwen38tui" in args or "qwen38-flash/.venv" in args:
                continue
            procs.append({"pid": int(pid), "rss": int(rss) * 1024, "comm": comm, "args": args[:120]})
    return procs


def probe() -> HardwareInfo:
    hw = HardwareInfo()
    hw.cpu_model, hw.cores_physical, hw.threads_logical = _cpu()
    mi = _meminfo()
    hw.mem_total = mi.get("MemTotal", 0)
    hw.mem_available = mi.get("MemAvailable", 0)
    hw.mem_cached = mi.get("Cached", 0)
    hw.swap_total = mi.get("SwapTotal", 0)
    g = _gpu()
    hw.gpu_name, hw.vram_total, hw.vram_used, hw.gtt_total, hw.gtt_used = g["name"], g["vram_total"], g["vram_used"], g["gtt_total"], g["gtt_used"]
    hw.gfx_target, hw.gpu_perf_level = g["gfx"], g["perf_level"]
    hw.rocm_version = _rocm_version()
    hw.kernel = _read("/proc/sys/kernel/osrelease")
    hw.cmdline = _read("/proc/cmdline")
    hw.governor = _read("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
    hw.epp = _read("/sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference")
    hw.platform_profile = _read("/sys/firmware/acpi/platform_profile")
    hw.thp = _read("/sys/kernel/mm/transparent_hugepage/enabled")
    if shutil.which("tuned-adm"):
        m = re.search(r"Current active profile:\s*(\S+)", _run(["tuned-adm", "active"]))
        hw.tuned_profile = m.group(1) if m else ""
    if shutil.which("powerprofilesctl"):
        hw.ppd_profile = _run(["powerprofilesctl", "get"]).strip()
    hw.primary_ip = _primary_ip()
    hw.hostname = _read("/etc/hostname") or os.uname().nodename
    hw.other_llm_procs = _other_llm_procs()
    hw.tips = make_tips(hw)
    return hw


def make_tips(hw: HardwareInfo) -> list[Tip]:
    tips: list[Tip] = []
    # Kernel-Parameter für großes GTT
    if "amdgpu.gttsize" in hw.cmdline:
        tips.append(Tip("ok", "GTT", "amdgpu.gttsize ist gesetzt – die iGPU darf fast den gesamten RAM als GTT nutzen."))
    else:
        tips.append(Tip("warnung", "GTT", "amdgpu.gttsize fehlt in der Kernel-Cmdline; ohne ihn sieht ROCm nur ~50% des RAM.",
                        "sudo grubby --update-kernel=ALL --args='amd_iommu=off amdgpu.gttsize=126976 ttm.pages_limit=32505856'"))
    if "ttm.pages_limit" not in hw.cmdline:
        tips.append(Tip("hinweis", "TTM", "ttm.pages_limit nicht gesetzt (Limit für pinnbare Seiten).",
                        "sudo grubby --update-kernel=ALL --args='ttm.pages_limit=32505856'"))
    # Governor / Profile
    if hw.governor and hw.governor != "performance":
        tips.append(Tip("hinweis", "CPU-Governor", f"Governor '{hw.governor}' (EPP: {hw.epp or '?'}). Für Benchmarks/Serverbetrieb 'performance' setzen "
                        "(hilft v.a. Prompt-Processing & Sampling; Decode ist speicherbandbreiten-limitiert).",
                        "sudo tuned-adm profile throughput-performance   # oder: sudo cpupower frequency-set -g performance"))
    else:
        tips.append(Tip("ok", "CPU-Governor", f"Governor '{hw.governor}'."))
    if hw.tuned_profile and hw.tuned_profile not in ("throughput-performance", "accelerator-performance", "latency-performance"):
        tips.append(Tip("hinweis", "tuned", f"tuned-Profil '{hw.tuned_profile}' aktiv.", "sudo tuned-adm profile accelerator-performance"))
    if hw.platform_profile and hw.platform_profile != "performance":
        tips.append(Tip("hinweis", "Platform-Profile", f"ACPI platform_profile = '{hw.platform_profile}' (TDP-Limit).",
                        "echo performance | sudo tee /sys/firmware/acpi/platform_profile"))
    if hw.gpu_perf_level and hw.gpu_perf_level not in ("auto", "high", "profile_peak"):
        tips.append(Tip("hinweis", "GPU-DPM", f"power_dpm_force_performance_level = '{hw.gpu_perf_level}'."))
    # THP
    if hw.thp and "[never]" in hw.thp:
        tips.append(Tip("hinweis", "THP", "Transparent Hugepages sind aus; 'madvise' oder 'always' kann große mmap-Modelle beschleunigen.",
                        "echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/enabled"))
    # Störprozesse
    big = [p for p in hw.other_llm_procs if p["rss"] > 2 * GIB]
    if big:
        names = ", ".join(f"{p['comm']}({p['pid']}, {p['rss'] / GIB:.1f} GiB)" for p in big[:4])
        tips.append(Tip("warnung", "Speicher", f"Andere LLM-Prozesse belegen Speicher: {names}", "pkill -f llama-server   # bzw. betreffende PID beenden"))
    # GTT-Größe vs RAM
    if hw.gtt_total and hw.gtt_total < 0.8 * hw.mem_total:
        tips.append(Tip("warnung", "GTT", f"GTT ({hw.gtt_total / GIB:.0f} GiB) ist deutlich kleiner als der RAM ({hw.mem_total / GIB:.0f} GiB)."))
    return tips
