"""Benchmarks aus dem TUI: llama-bench (pp/tg ohne MTP) und Server-Messung (mit MTP, Draft-Akzeptanz)."""
from __future__ import annotations

import asyncio
import json
import os
import signal
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from .config import Command, ServerConfig, build_command
from .discovery import Inventory, STATE_DIR
from .hardware import HardwareInfo
from .server import ServerClient, ServerProcess

RESULTS = STATE_DIR / "bench" / "results.jsonl"

PROMPTS = [
    ("code", "Schreibe eine vollständige Python-Klasse `LRUCache` mit get/put in O(1), Typannotationen, Docstrings und 5 pytest-Tests."),
    ("prosa", "Erkläre einem Erstsemester in etwa 400 Wörtern, wie ein Mixture-of-Experts-Sprachmodell funktioniert und warum es schneller ist als ein dichtes Modell gleicher Größe."),
    ("reasoning", "Ein Zug fährt um 8:00 mit 80 km/h von A nach B (240 km). Ein zweiter Zug fährt um 8:30 mit 120 km/h von B nach A. Wann und wo treffen sie sich? Rechne Schritt für Schritt."),
]


@dataclass
class BenchResult:
    kind: str                      # "llama-bench" | "server"
    name: str
    when: str
    engine: str
    quant: str
    ctx: int
    ctk: str
    ctv: str
    ubatch: int
    mtp: str                       # "aus" | "n3 p0.75"
    pp_tps: float = 0.0
    tg_tps: float = 0.0
    accept: float | None = None
    load_s: float = 0.0
    details: dict[str, Any] = field(default_factory=dict)
    error: str = ""
    users: int = 1                 # Mehrnutzer-Test: gleichzeitige Anfragen
    agg_tps: float = 0.0           # Summe der Decode-Tokens aller Nutzer pro Sekunde Wandzeit
    ttft_p50: float = 0.0          # Zeit bis zum ersten Token (s)
    ttft_p95: float = 0.0
    crosstalk: int = 0             # Antworten, die ein fremdes Codewort enthalten / das eigene nicht

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_results() -> list[BenchResult]:
    out: list[BenchResult] = []
    if RESULTS.exists():
        for line in RESULTS.read_text().splitlines():
            try:
                d = json.loads(line)
                out.append(BenchResult(**{k: d.get(k) for k in BenchResult.__dataclass_fields__ if k in d}))
            except Exception:
                continue
    return out


def _append(r: BenchResult) -> None:
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS.open("a") as f:
        f.write(json.dumps(r.to_dict(), ensure_ascii=False) + "\n")


def _tag(cfg: ServerConfig) -> str:
    return f"n{cfg.spec_draft_n_max} p{cfg.spec_draft_p_min:g}" if cfg.mtp_enabled else "aus"


# ----------------------------------------------------------------------------------------------
async def run_llama_bench(cfg: ServerConfig, inv: Inventory, hw: HardwareInfo | None, on_line: Callable[[str], None],
                          n_prompt: int = 512, n_gen: int = 128, reps: int = 2, depth: int = 0) -> BenchResult:
    """pp/tg via llama-bench (ohne MTP – llama-bench kennt keine Draft-Modelle)."""
    cmd = build_command(cfg, inv, hw)
    r = cmd.resolved
    res = BenchResult("llama-bench", f"pp{n_prompt}/tg{n_gen}" + (f"@d{depth}" if depth else ""), datetime.now().isoformat(timespec="seconds"),
                      r.engine.key if r.engine else "?", r.model.quant if r.model else "?", cfg.ctx_size, cfg.cache_type_k, cfg.cache_type_v,
                      cfg.ubatch_size, "aus")
    if not (r.engine and r.model):
        res.error = "; ".join(cmd.errors) or "Engine/Modell fehlt"
        return res
    bench = r.engine.bench_argv()
    if not bench:
        res.error = "Kein llama-bench für diese Engine"
        return res
    argv = bench + ["-m", str(r.model.path), "-ngl", str(cfg.n_gpu_layers), "-t", str(cfg.threads), "-fa", cfg.flash_attn,
                    "-ctk", cfg.cache_type_k, "-ctv", cfg.cache_type_v, "-b", str(cfg.batch_size), "-ub", str(cfg.ubatch_size),
                    "-p", str(n_prompt), "-n", str(n_gen), "-r", str(reps), "-o", "json", "--progress"]
    # Lade-Optionen wie beim Server (sonst stimmt die Speicherprüfung nicht); EngramHalo kennt nur --lazy-mode
    if cfg.tensor_read_lazy != "auto":
        argv += ["--lazy-mode" if r.engine.fast_lazy_ple else "--tensor-read-lazy", cfg.tensor_read_lazy]
    if cfg.load_mode != "auto":
        argv += ["-lm", cfg.load_mode]
    if cfg.no_host:
        argv += ["--no-host"]
    if cfg.ple_cpu_override:
        argv += ["-ot", "per_layer_token_embd.weight=CPU"]
    if depth:
        argv += ["-d", str(depth)]
    env = dict(os.environ)
    env.update(cmd.env)
    on_line("$ " + " ".join(argv))
    t0 = time.time()
    proc = await asyncio.create_subprocess_exec(*argv, env=env, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                                                start_new_session=True)
    out_chunks: list[bytes] = []

    async def pump_err() -> None:
        assert proc.stderr
        while True:
            line = await proc.stderr.readline()
            if not line:
                break
            on_line(line.decode(errors="replace").rstrip())

    async def pump_out() -> None:
        assert proc.stdout
        while True:
            chunk = await proc.stdout.read(65536)
            if not chunk:
                break
            out_chunks.append(chunk)

    try:
        await asyncio.gather(pump_err(), pump_out())
        code = await proc.wait()
    except asyncio.CancelledError:
        # Worker abgebrochen (App-Ende): den 70–100-GB-Benchmark nicht verwaisen lassen
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        raise
    res.load_s = time.time() - t0
    try:
        data = json.loads(b"".join(out_chunks).decode())
        for row in data:
            if row.get("n_prompt"):
                res.pp_tps = float(row.get("avg_ts", 0))
            elif row.get("n_gen"):
                res.tg_tps = float(row.get("avg_ts", 0))
        res.details = {"rows": data}
    except Exception as e:
        res.error = f"exit {code}, JSON: {e}"
    _append(res)
    return res


# ----------------------------------------------------------------------------------------------
def _mem_available() -> int:
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) * 1024
    except OSError:
        pass
    return 0


async def _memory_watchdog(sp: ServerProcess, threshold_gib: float, on_line: Callable[[str], None], interval: float = 0.5) -> None:
    """Stoppt den Benchmark-Server hart, bevor der Kernel-OOM-Killer zuschlägt (auch außerhalb des TUI)."""
    if threshold_gib <= 0:
        return
    thr = int(threshold_gib * 2**30)
    while sp.running:
        avail = _mem_available()
        if 0 < avail < thr:
            on_line(f"[memguard] MemAvailable {avail / 2**30:.1f} GiB < {threshold_gib:.1f} GiB – Server wird gestoppt")
            await sp.stop(grace=1)
            return
        await asyncio.sleep(interval)


async def run_server_bench(cfg: ServerConfig, inv: Inventory, hw: HardwareInfo | None, on_line: Callable[[str], None],
                           max_tokens: int = 400, prompts: list[tuple[str, str]] | None = None,
                           should_abort: Callable[[], bool] | None = None) -> BenchResult:
    """Startet den Server mit der Konfiguration (inkl. MTP), misst tg/pp und Draft-Akzeptanz über echte Chat-Requests."""
    cfg = cfg.copy(host="127.0.0.1", port=cfg.port + 19, webui=False, metrics=False)
    cmd = build_command(cfg, inv, hw)
    r = cmd.resolved
    res = BenchResult("server", f"chat x{len(prompts or PROMPTS)}", datetime.now().isoformat(timespec="seconds"),
                      r.engine.key if r.engine else "?", r.model.quant if r.model else "?", cfg.ctx_size, cfg.cache_type_k, cfg.cache_type_v,
                      cfg.ubatch_size, _tag(cfg))
    if not cmd.ok:
        res.error = "; ".join(cmd.errors)
        return res
    sp = ServerProcess()
    client = ServerClient("127.0.0.1", cfg.port)
    t0 = time.time()
    wd: asyncio.Task | None = None
    try:
        await sp.start(cmd, on_line)
        wd = asyncio.create_task(_memory_watchdog(sp, cfg.mem_guard_gib, on_line))
        ok = await client.wait_ready(timeout=900, should_abort=lambda: (not sp.running) or (should_abort() if should_abort else False))
        if not ok:
            res.error = "Server nicht bereit (Log prüfen)"
            return res
        res.load_s = time.time() - t0
        await client.chat("Sag nur: bereit.", max_tokens=16)
        runs = []
        for key, p in (prompts or PROMPTS):
            if should_abort and should_abort():
                break
            out = await client.chat(p, max_tokens=max_tokens)
            t = out["timings"]
            runs.append({"prompt": key, **t, "wall": out["wall"]})
            dn, da = t.get("draft_n", 0), t.get("draft_n_accepted", 0)
            on_line(f"[bench] {key}: pp {t.get('prompt_per_second', 0):.1f} t/s, tg {t.get('predicted_per_second', 0):.2f} t/s, n={t.get('predicted_n')}"
                    + (f", draft {da}/{dn} ({da / dn:.0%})" if dn else ""))
        if runs:
            res.tg_tps = sum(x.get("predicted_per_second", 0) for x in runs) / len(runs)
            res.pp_tps = sum(x.get("prompt_per_second", 0) for x in runs) / len(runs)
            dn = sum(x.get("draft_n", 0) for x in runs)
            da = sum(x.get("draft_n_accepted", 0) for x in runs)
            res.accept = da / dn if dn else None
            res.details = {"runs": runs, "stats": {"compute_mib": sp.stats.compute_buffer_mib, "kv_mib": sp.stats.kv_buffer_mib}}
            sp.record_measurements(res.quant, cfg.ubatch_size, cfg.flash_attn)
    except asyncio.CancelledError:
        await sp.stop(grace=2)
        raise
    except Exception as e:
        res.error = f"{e.__class__.__name__}: {e}"
    finally:
        if wd:
            wd.cancel()
        if sp.running:
            await sp.stop(grace=30)
    _append(res)
    return res


# ----------------------------------------------------------------------------------------------
def sweep_candidates(base: ServerConfig) -> list[tuple[str, ServerConfig]]:
    """Kandidaten für das Auto-Tuning (MTP-Parameter) auf Basis der aktuellen Konfiguration."""
    cands: list[tuple[str, ServerConfig]] = [("ohne MTP", base.copy(mtp_enabled=False))]
    for n_max, p_min in ((2, 0.75), (3, 0.75), (3, 0.0), (4, 0.75), (5, 0.5)):
        cands.append((f"MTP n{n_max} p{p_min:g}", base.copy(mtp_enabled=True, spec_draft_n_max=n_max, spec_draft_p_min=p_min)))
    return cands


# ----------------------------------------------------------------------------------------------
# Mehrnutzer-Benchmark (parallele Slots, Continuous Batching)
# ----------------------------------------------------------------------------------------------
import random
import statistics

USER_TASKS = [
    "Schreibe eine Python-Funktion, die eine Liste von Zahlen stabil nach dem Betrag sortiert, mit Docstring und drei Beispielen.",
    "Erkläre in etwa 200 Wörtern, warum Unified Memory für lokale Sprachmodelle praktisch ist.",
    "Ein Zug fährt um 9:00 mit 90 km/h von A nach B (270 km), ein zweiter um 9:30 mit 135 km/h von B nach A. Wann treffen sie sich? Rechne Schritt für Schritt.",
    "Schreibe eine kurze SQL-Abfrage, die die fünf umsatzstärksten Kunden des letzten Quartals liefert, und erkläre jede Zeile.",
    "Fasse in fünf Stichpunkten zusammen, wie ein KV-Cache in Transformern funktioniert.",
    "Schreibe ein Bash-Skript, das alle .log-Dateien älter als 7 Tage in ein Archiv verschiebt, mit Kommentaren.",
    "Nenne drei typische Fehler beim Einsatz von Mixture-of-Experts-Modellen und wie man sie vermeidet.",
    "Schreibe eine kleine TypeScript-Funktion, die ein Datum als ISO-Woche formatiert, plus zwei Tests.",
]


def make_user_prompts(n: int, seed: int = 0) -> list[tuple[str, str]]:
    """n Prompts mit eindeutigem Codewort (für die Mix-up-Prüfung): [(codewort, prompt), ...]."""
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        code = f"KW{i + 1}{rnd.randint(1000, 9999)}"
        task = USER_TASKS[i % len(USER_TASKS)]
        out.append((code, f"Du bist Nutzer {i + 1}. Dein Codewort ist {code}. Beginne deine Antwort mit dem Codewort. Aufgabe: {task}"))
    return out


def check_crosstalk(own: str, text: str, all_codes: list[str]) -> bool:
    """True, wenn die Antwort ein fremdes Codewort enthält oder das eigene fehlt (Slot-Mix-up)."""
    blob = text or ""
    if own not in blob:
        return True
    return any(c in blob for c in all_codes if c != own)


def aggregate_level(per_user: list[dict[str, Any]], wall: float) -> dict[str, float]:
    gen = sum(int(u.get("predicted_n") or 0) for u in per_user)
    tg = [float(u.get("predicted_per_second") or 0) for u in per_user]
    ttft = sorted(float(u.get("ttft") or 0) for u in per_user)
    pp = [float(u.get("prompt_per_second") or 0) for u in per_user if u.get("prompt_per_second")]

    def pct(vals: list[float], q: float) -> float:
        if not vals:
            return 0.0
        k = max(0, min(len(vals) - 1, round(q * (len(vals) - 1))))
        return vals[k]

    return {"agg_tps": gen / wall if wall > 0 else 0.0, "gen_tokens": gen, "user_tg_mean": statistics.mean(tg) if tg else 0.0,
            "user_tg_min": min(tg) if tg else 0.0, "ttft_p50": pct(ttft, 0.5), "ttft_p95": pct(ttft, 0.95),
            "pp_mean": statistics.mean(pp) if pp else 0.0, "wall": wall}


async def run_parallel_bench(cfg: ServerConfig, inv: Inventory, hw: HardwareInfo | None, on_line: Callable[[str], None],
                             levels: tuple[int, ...] = (1, 2, 4, 8), max_tokens: int = 256, keep_mtp: bool = False,
                             min_ctx_per_slot: int = 8192, should_abort: Callable[[], bool] | None = None) -> list[BenchResult]:
    """Ein Server mit -np max(levels); dann je Stufe N gleichzeitige Chat-Anfragen (asyncio.gather).
    Misst Gesamtdurchsatz, Durchsatz je Nutzer, Zeit bis zum ersten Token und prüft per Codewort auf Slot-Mix-ups."""
    n_par = max(levels)
    cfg = cfg.copy(host="127.0.0.1", port=cfg.port + 29, webui=False, metrics=False, n_parallel=n_par,
                   mtp_enabled=cfg.mtp_enabled and keep_mtp, spec_extra_types=cfg.spec_extra_types if keep_mtp else "")
    if cfg.ctx_size // n_par < min_ctx_per_slot:
        cfg.ctx_size = min_ctx_per_slot * n_par
        on_line(f"[bench] Kontext auf {cfg.ctx_size} erhöht ({min_ctx_per_slot} je Slot × {n_par} Slots)")
    cmd = build_command(cfg, inv, hw)
    r = cmd.resolved
    results: list[BenchResult] = []
    base = dict(when=datetime.now().isoformat(timespec="seconds"), engine=r.engine.key if r.engine else "?",
                quant=r.model.quant if r.model else "?", ctx=cfg.ctx_size, ctk=cfg.cache_type_k, ctv=cfg.cache_type_v,
                ubatch=cfg.ubatch_size, mtp=_tag(cfg))
    if not cmd.ok:
        res = BenchResult("parallel", "Mehrnutzer", **base)
        res.error = "; ".join(cmd.errors)
        return [res]
    for w in cmd.warnings:
        on_line("[bench] ⚠ " + w)
    sp = ServerProcess()
    client = ServerClient("127.0.0.1", cfg.port)
    t0 = time.time()
    wd: asyncio.Task | None = None
    try:
        await sp.start(cmd, on_line)
        wd = asyncio.create_task(_memory_watchdog(sp, cfg.mem_guard_gib, on_line))
        ok = await client.wait_ready(timeout=900, should_abort=lambda: (not sp.running) or (should_abort() if should_abort else False))
        if not ok:
            res = BenchResult("parallel", "Mehrnutzer", **base)
            res.error = "Server nicht bereit (Log prüfen)"
            _append(res)
            return [res]
        load_s = time.time() - t0
        await client.chat("Sag nur: bereit.", max_tokens=8)
        for n in levels:
            if should_abort and should_abort():
                break
            prompts = make_user_prompts(n, seed=n)
            codes = [c for c, _ in prompts]
            on_line(f"[bench] {n} Nutzer gleichzeitig, je max {max_tokens} Tokens …")
            t_level = time.time()

            async def one(i: int, code: str, prompt: str) -> dict[str, Any]:
                try:
                    out = await client.chat(prompt, max_tokens=max_tokens, timeout=1800)
                except Exception as e:
                    return {"user": i, "code": code, "error": f"{e.__class__.__name__}: {e}", "ttft": 0.0}
                t = out["timings"]
                return {"user": i, "code": code, "ttft": out["ttft"], "wall": out["wall"],
                        "crosstalk": check_crosstalk(code, out["text"] + "\n" + out["reasoning"], codes),
                        "text_head": out["text"][:80], **t}

            per_user = list(await asyncio.gather(*(one(i, c, p) for i, (c, p) in enumerate(prompts))))
            wall = time.time() - t_level
            agg = aggregate_level([u for u in per_user if "error" not in u], wall)
            errors = [u for u in per_user if "error" in u]
            mixups = sum(1 for u in per_user if u.get("crosstalk"))
            res = BenchResult("parallel", f"{n} Nutzer", **base)
            res.users, res.tg_tps, res.pp_tps = n, agg["user_tg_mean"], agg["pp_mean"]
            res.agg_tps, res.ttft_p50, res.ttft_p95, res.crosstalk, res.load_s = agg["agg_tps"], agg["ttft_p50"], agg["ttft_p95"], mixups, load_s
            res.details = {"per_user": per_user, "aggregate": agg, "n_parallel": n_par, "ctx_per_slot": cfg.ctx_size // n_par}
            if errors:
                res.error = f"{len(errors)} Anfragen fehlgeschlagen: {errors[0]['error'][:80]}"
            on_line(f"[bench] {n} Nutzer: Σ {agg['agg_tps']:.1f} t/s · je Nutzer Ø {agg['user_tg_mean']:.1f} (min {agg['user_tg_min']:.1f}) t/s · "
                    f"TTFT p50 {agg['ttft_p50']:.1f}s / p95 {agg['ttft_p95']:.1f}s · {agg['gen_tokens']} Tokens in {wall:.0f}s"
                    + (f" · ⚠ {mixups} Mix-ups" if mixups else " · keine Mix-ups") + (f" · {res.error}" if res.error else ""))
            _append(res)
            results.append(res)
    except asyncio.CancelledError:
        await sp.stop(grace=2)
        raise
    except Exception as e:
        res = BenchResult("parallel", "Mehrnutzer", **base)
        res.error = f"{e.__class__.__name__}: {e}"
        _append(res)
        results.append(res)
    finally:
        if wd:
            wd.cancel()
        if sp.running:
            await sp.stop(grace=30)
    return results
