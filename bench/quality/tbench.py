#!/usr/bin/env python3
"""Terminal-Bench-Mini-20 gegen den lokalen Qwen3.8-Flash-Next fahren.

Startet den Server mit einer Konfiguration aus dem TUI (Preset oder Profil, mit Overrides),
wartet auf /health, ruft den Runner aus bench/quality/terminal-bench-mini auf und räumt danach auf.
Der Server läuft unter bench/memguard.py, damit ein Container-Speicherfresser nicht die
ganze Maschine in den Kernel-OOM zieht.

  bench/quality/tbench.py --tier smoke                       # 1 Aufgabe, Rauchtest
  bench/quality/tbench.py --tier full --quant UD-IQ4_XS      # alle 20 Aufgaben
  bench/quality/tbench.py --task fix-git --attempts 1        # eine Aufgabe
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
TBM = HERE / "terminal-bench-mini"
MEMGUARD = PROJECT / "bench" / "memguard.py"
sys.path.insert(0, str(PROJECT))

GIB = 2**30


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def http_json(url: str, timeout: float = 5):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.load(r)


def wait_ready(base: str, deadline: float) -> bool:
    last = ""
    while time.time() < deadline:
        try:
            d = http_json(base + "/health", timeout=5)
            if d.get("status") == "ok":
                return True
            last = str(d)
        except (urllib.error.URLError, OSError, ValueError) as e:
            last = e.__class__.__name__
        time.sleep(3)
    log(f"Server wurde nicht bereit (zuletzt: {last})")
    return False


UBUNTU_HOSTS = ("archive.ubuntu.com", "security.ubuntu.com")
DEFAULT_MIRROR = "ftp.fau.de"


def probe_seconds(url: str, timeout: float = 8.0) -> float:
    """Antwortzeit einer HEAD-artigen Anfrage; inf bei Fehler."""
    t0 = time.time()
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout):
            return time.time() - t0
    except Exception:
        return float("inf")


def apt_mirror_hosts(mode: str, slow_after: float = 3.0) -> list[str]:
    """/etc/hosts-Einträge, die archive.ubuntu.com auf einen schnellen Spiegel legen.

    'off' = nichts, 'auto' = nur wenn archive.ubuntu.com langsam antwortet, sonst der
    angegebene Spiegel-Hostname. Ubuntu-Spiegel liefern die Pfade unabhängig vom
    Host-Header, deshalb genügt der Eintrag in /etc/hosts des Containers.
    """
    if mode in ("off", "aus", ""):
        return []
    host = DEFAULT_MIRROR if mode == "auto" else mode
    if mode == "auto":
        dt = probe_seconds("http://archive.ubuntu.com/ubuntu/dists/noble/Release")
        if dt <= slow_after:
            log(f"   apt-Spiegel     nicht nötig (archive.ubuntu.com antwortet in {dt:.1f}s)")
            return []
        wie = "antwortet nicht" if dt == float("inf") else f"braucht {dt:.1f}s"
        log(f"   apt-Spiegel     archive.ubuntu.com {wie} -> {host}")
    try:
        ip = socket.getaddrinfo(host, 80, socket.AF_INET, socket.SOCK_STREAM)[0][4][0]
    except OSError as e:
        log(f"   WARNUNG: Spiegel {host} nicht auflösbar ({e}); apt bleibt beim Original.")
        return []
    if mode != "auto":
        log(f"   apt-Spiegel     {host} ({ip})")
    return [f"{h}:{ip}" for h in UBUNTU_HOSTS]


SPINNER = "\u280b\u2819\u2839\u2838\u283c\u2834\u2826\u2827\u2807\u280f"


def run_filtered(argv: list[str], cwd: str, raw: bool = False, every: float = 60.0,
                 env: dict | None = None) -> int:
    """Wie subprocess.call, aber die Fortschrittsbalken von Harbor werden ausgedünnt:
    Spinner-Frames landen höchstens alle `every` Sekunden im Log statt zehnmal pro Sekunde."""
    if raw:
        return subprocess.call(argv, cwd=cwd, env=env)

    proc = subprocess.Popen(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, bufsize=0, start_new_session=True)
    out, last, buf = sys.stdout.buffer, 0.0, b""
    assert proc.stdout
    while True:
        try:
            chunk = proc.stdout.read(4096)
        except KeyboardInterrupt:
            log("   breche den Benchmark ab …")
            stop_tree(proc.pid, grace=20.0)
            raise
        if not chunk:
            break
        buf += chunk
        parts = buf.replace(b"\r", b"\n").split(b"\n")
        buf = parts.pop()
        for part in parts:
            text = part.decode("utf-8", "replace")
            if any(c in text for c in SPINNER):
                now = time.time()
                if now - last < every:
                    continue
                last = now
            if text.strip():
                out.write(text.encode("utf-8", "replace") + b"\n")
                out.flush()
    if buf.strip():
        out.write(buf + b"\n")
        out.flush()
    return proc.wait()


def mem_available() -> int:
    with open("/proc/meminfo") as f:
        for line in f:
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) * 1024
    return 0


def leftover_servers() -> list[int]:
    """Noch laufende llama-Prozesse dieses Nutzers (Namen aus /proc, kein pgrep-Rätselraten)."""
    out = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            if (entry / "comm").read_text().strip() in ("llama", "llama-server"):
                out.append(int(entry.name))
        except OSError:
            continue
    return out


def alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def descendants(pid: int) -> list[int]:
    """Alle Nachfahren eines Prozesses (über /proc), Kinder zuerst."""
    kids: dict[int, list[int]] = {}
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            stat = (entry / "stat").read_text()
            ppid = int(stat[stat.rindex(")") + 2:].split()[1])
        except (OSError, ValueError, IndexError):
            continue
        kids.setdefault(ppid, []).append(int(entry.name))
    out, queue = [], [pid]
    while queue:
        for child in kids.get(queue.pop(0), []):
            out.append(child)
            queue.append(child)
    return out


def kill_group(pid: int, sig: int) -> None:
    try:
        os.killpg(os.getpgid(pid), sig)
    except OSError:
        try:
            os.kill(pid, sig)
        except OSError:
            pass


def wait_gone(pids: list[int], seconds: float) -> bool:
    end = time.time() + seconds
    while time.time() < end:
        if not any(alive(p) for p in pids):
            return True
        time.sleep(0.5)
    return not any(alive(p) for p in pids)


def stop_tree(pid: int, grace: float = 30.0) -> None:
    """Server beenden: erst freundlich, dann hart – und zwar direkt, nicht über den Wächter.

    memguard startet den Server in einer eigenen Sitzung; ein Signal an die Prozessgruppe des
    Wächters erreicht ihn deshalb nicht. Die Nachfahren werden gesucht und einzeln beendet.
    Der Server muss weg sein, bevor der nächste Quant startet, sonst passt das Modell nicht mehr
    in den Speicher.
    """
    kids = descendants(pid)
    for k in kids:
        kill_group(k, signal.SIGINT)
    if not wait_gone(kids, grace):
        for k in kids:
            kill_group(k, signal.SIGKILL)
        wait_gone(kids, 15.0)
    kill_group(pid, signal.SIGTERM)
    if not wait_gone([pid], 10.0):
        kill_group(pid, signal.SIGKILL)


def profile_label(cfg) -> str:
    parts = []
    if cfg.mtp_enabled:
        parts.append(f"mtp{cfg.spec_draft_n_max}")
        if "ngram" in cfg.spec_extra_types:
            parts.append("ngram")
    else:
        parts.append("no-mtp")
    parts.append(f"thinking-{cfg.reasoning_effort}" if cfg.thinking else "no-thinking")
    if cfg.n_parallel > 1:
        parts.append(f"np{cfg.n_parallel}")
    return "-".join(parts)


def _term(signum, frame):  # pragma: no cover - Signalpfad
    raise KeyboardInterrupt


def main() -> int:
    signal.signal(signal.SIGTERM, _term)
    ap = argparse.ArgumentParser(description="Terminal-Bench-Mini-20 gegen den lokalen Server")
    g = ap.add_argument_group("Server")
    g.add_argument("--preset", default="eh-agent", help="Preset für den Server (Default: eh-agent)")
    g.add_argument("--profile", default="", help="gespeichertes Profil statt Preset")
    g.add_argument("--quant", default="", help="Quant überschreiben, z.B. UD-IQ4_XS")
    g.add_argument("--ctx", type=int, default=0, help="Kontext (gesamt über alle Slots) überschreiben")
    g.add_argument("--no-mtp", action="store_true", help="spekulatives Decoding abschalten")
    g.add_argument("--reasoning-effort", default="", choices=["", "low", "medium", "xhigh"])
    g.add_argument("--min-avail-gib", type=float, default=0.0,
                   help="Speicher-Wächter: Server killen, wenn MemAvailable darunter fällt (Default: aus dem Preset)")
    g.add_argument("--reserve-gib", type=float, default=8.0,
                   help="Spielraum, den die Docker-Container brauchen; darunter wird gewarnt (Default 8)")
    g.add_argument("--use-running", action="store_true", help="keinen Server starten, laufenden benutzen")
    g.add_argument("--endpoint", default="", help="Endpunkt überschreiben (Default: aus der Konfiguration)")

    b = ap.add_argument_group("Benchmark")
    b.add_argument("--tier", default="full", choices=["smoke", "full"])
    b.add_argument("--task", default="", help="eine einzelne Aufgabe statt einer Stufe")
    b.add_argument("--tasks", default="", help="mehrere Aufgaben nacheinander: Liste (a,b,c) oder @datei")
    b.add_argument("--attempts", type=int, default=0, help="Versuche je Aufgabe (Default 2 = pass@2)")
    b.add_argument("--concurrency", type=int, default=0, help="parallele Aufgaben (braucht Slots: --slots)")
    b.add_argument("--slots", type=int, default=0, help="Server-Slots (-np); Default: wie --concurrency")
    b.add_argument("--agent-timeout", type=int, default=0, help="Sekunden je Versuch (Default 10800)")
    b.add_argument("--results-dir", default=str(PROJECT / "state" / "quality" / "tbench"))
    b.add_argument("--job-name", default="")
    b.add_argument("--tag", default="", help="zusätzliche Kennung des Laufs (z.B. Engine-Patch), landet in der Ergebnis-Identität")
    b.add_argument("--dry-run", action="store_true", help="nur Kommandos zeigen, nichts starten")
    b.add_argument("--raw-output", action="store_true", help="Ausgabe von Harbor nicht ausdünnen (Spinner-Frames behalten)")
    b.add_argument("--apt-mirror", default="auto",
                   help="Spiegel für archive.ubuntu.com in den Containern: auto (Default, nur wenn langsam), off oder ein Hostname")
    b.add_argument("rest", nargs=argparse.REMAINDER, help="-- weitere Argumente für terminal_bench.py")
    a = ap.parse_args()

    if not (TBM / "terminal_bench.py").is_file():
        log(f"{TBM} fehlt – erst 'bench/quality/fetch.sh' laufen lassen.")
        return 2

    from qwen38tui.config import ServerConfig, build_command, load_profile
    from qwen38tui.discovery import discover_all
    from qwen38tui.hardware import probe
    from qwen38tui.memory import estimate, fits
    from qwen38tui.presets import get_preset

    if a.profile:
        cfg = load_profile(a.profile)
    else:
        pr = get_preset(a.preset)
        if not pr:
            log(f"Unbekanntes Preset: {a.preset}")
            return 2
        cfg = pr.apply()
    slots = a.slots or a.concurrency or cfg.n_parallel
    over: dict = {"n_parallel": max(1, slots)}
    if a.quant:
        over["quant"] = a.quant
    if a.ctx:
        over["ctx_size"] = a.ctx
    if a.no_mtp:
        over["mtp_enabled"] = False
    if a.reasoning_effort:
        over["reasoning_effort"] = a.reasoning_effort
    cfg = cfg.copy(**over)

    inv, hw = discover_all(), probe()
    cmd = build_command(cfg, inv, hw, fits=lambda m: fits(cfg, m, None, hw))
    if not cmd.ok:
        for e in cmd.errors:
            log("FEHLER: " + e)
        return 1
    r = cmd.resolved
    est = estimate(cfg, r.model, r.mtp, hw, r.engine.backend if r.engine else "hip",
                   bool(r.engine and r.engine.fast_lazy_ple))
    ctx_per_slot = cfg.ctx_size // max(1, cfg.n_parallel)
    concurrency = a.concurrency or 1

    log("== Server")
    log(f"   Engine        {r.engine.label if r.engine else '-'}")
    log(f"   Modell        {r.model.quant if r.model else '-'}  ({r.model.size_gib:.1f} GiB)" if r.model else "")
    log(f"   MTP           {r.mtp.path.name if (cfg.mtp_enabled and r.mtp) else 'aus'}")
    log(f"   Kontext       {cfg.ctx_size} gesamt, {ctx_per_slot} je Slot ({cfg.n_parallel} Slots)")
    for k, v in est.rows():
        log(f"   {k:34} {v}")
    log(f"   Bewertung     {est.verdict}")
    for w in cmd.warnings:
        log("   WARNUNG: " + w)
    if est.verdict == "zu groß":
        log("FEHLER: passt nicht in den Speicher.")
        return 1
    head = est.headroom / GIB
    need = a.reserve_gib * max(1, concurrency)
    if head < need:
        log(f"   WARNUNG: nur {head:.1f} GiB Spielraum für {concurrency} Container "
            f"(empfohlen {need:.0f} GiB) – kleineren Quant oder weniger Kontext wählen.")

    host = r.host
    base = a.endpoint.rstrip("/") if a.endpoint else f"http://{host}:{cfg.port}"
    if base.endswith("/v1"):
        base = base[:-3]
    endpoint = base + "/v1"
    if any(h in base for h in ("127.0.0.1", "localhost")):
        log("   WARNUNG: Der Agent läuft in einem Docker-Container (Bridge-Netz) und erreicht "
            "127.0.0.1 des Hosts nicht. Server an die LAN-Adresse binden (Host in der Konfiguration).")

    runner = [sys.executable, "terminal_bench.py", "run",
              "--endpoint", endpoint,
              "--model", cfg.alias,
              "--context-length", str(ctx_per_slot),
              "--platform", "strix-halo",
              "--platform-name", "AMD Ryzen AI MAX+ 395 (Strix Halo)",
              "--model-name", "Qwen3.8-Flash-Next",
              "--engine", "llama.cpp",
              "--engine-version", (r.engine.version() if r.engine else "?"),
              "--backend", "rocm",
              "--backend-version", hw.rocm_version or "?",
              "--quant", (r.model.quant if r.model else "?"),
              "--inference-profile", profile_label(cfg)] + (["--tag", a.tag] if a.tag else []) + [
              "--results-dir", str(Path(a.results_dir).expanduser().resolve())]
    tasks: list[str] = []
    if a.tasks:
        if a.tasks.startswith("@"):
            tasks = [ln.strip() for ln in Path(a.tasks[1:]).read_text().splitlines()
                     if ln.strip() and not ln.startswith("#")]
        else:
            tasks = [t.strip() for t in a.tasks.split(",") if t.strip()]
    elif a.task:
        tasks = [a.task]
    if not tasks:
        runner += ["--tier", a.tier]
    if a.attempts:
        runner += ["--attempts", str(a.attempts)]
    if a.concurrency:
        runner += ["--concurrency", str(a.concurrency)]
    if a.agent_timeout:
        runner += ["--agent-timeout", str(a.agent_timeout)]
    if a.job_name and not (a.tasks or a.task):
        runner += ["--job-name", a.job_name]
    extra = [x for x in a.rest if x != "--"]
    runner += extra
    if cfg.api_key:
        runner += ["--api-key", cfg.api_key]

    guard = a.min_avail_gib or cfg.mem_guard_gib
    stamp = time.strftime("%Y%m%d-%H%M%S")
    logdir = PROJECT / "state" / "logs"
    logdir.mkdir(parents=True, exist_ok=True)
    srvlog = logdir / f"tbench-server-{stamp}.log"
    server_cmd = [sys.executable, str(MEMGUARD), "--min-avail-gib", str(guard),
                  "--csv", str(logdir / f"tbench-mem-{stamp}.csv"), "--"] + cmd.argv

    log("")
    log("== Benchmark")
    log("   " + " ".join(runner))
    if not a.use_running:
        log(f"   Server-Log    {srvlog}")
        log(f"   Wächter       SIGKILL bei MemAvailable < {guard:.1f} GiB")
    shim = HERE / "dockershim"
    renv = dict(os.environ)
    hosts = apt_mirror_hosts(a.apt_mirror)
    if hosts:
        renv["QWEN38_EXTRA_HOSTS"] = ",".join(hosts)
        renv["QWEN38_REAL_DOCKER"] = shutil.which("docker") or "/usr/bin/docker"
        renv["QWEN38_SHIM_DIR"] = str(PROJECT / "state" / "quality")
        renv["PATH"] = f"{shim}{os.pathsep}{renv.get('PATH', '')}"

    if a.dry_run:
        log("")
        log("$ " + cmd.shell())
        return 0

    proc = None
    try:
        if not a.use_running:
            env = dict(os.environ)
            env.update(cmd.env)
            fh = srvlog.open("w", buffering=1)
            fh.write("# " + cmd.shell() + "\n")
            t_start = time.time()
            proc = subprocess.Popen(server_cmd, env=env, stdout=fh, stderr=subprocess.STDOUT,
                                    start_new_session=True)
            log(f"   Server gestartet (pid {proc.pid}), warte auf /health …")
            if not wait_ready(base, time.time() + 1800):
                return 1
            log(f"   bereit nach {time.time() - t_start:.0f}s")
        else:
            if not wait_ready(base, time.time() + 30):
                log("FEHLER: kein laufender Server unter " + base)
                return 1
        t0 = time.time()
        if tasks:
            rc = 0
            for i, task in enumerate(tasks, 1):
                argv = list(runner) + ["--task", task]
                if a.job_name:
                    argv += ["--job-name", f"{a.job_name}-{task}"]
                log(f"-- [{i}/{len(tasks)}] {task}")
                t1 = time.time()
                one = run_filtered(argv, cwd=str(TBM), raw=a.raw_output, env=renv)
                log(f"-- {task}: exit {one} nach {(time.time() - t1) / 60:.0f} min")
                rc = rc or one
        else:
            rc = run_filtered(runner, cwd=str(TBM), raw=a.raw_output, env=renv)
        log(f"== fertig nach {(time.time() - t0) / 3600:.2f} h, exit {rc}")
        return rc
    except KeyboardInterrupt:
        log("== abgebrochen")
        for q in descendants(os.getpid()):
            kill_group(q, signal.SIGKILL)
        return 130
    finally:
        if proc and proc.poll() is None:
            log("   stoppe Server …")
            t_stop = time.time()
            stop_tree(proc.pid, grace=30.0)
            try:
                proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                log("   WARNUNG: Wächter reagiert nicht mehr, Prozess bleibt zurück.")
            rest = leftover_servers()
            if rest:
                log(f"   WARNUNG: Server-Prozesse leben noch: {rest} – werden hart beendet.")
                for q in rest:
                    kill_group(q, signal.SIGKILL)
                wait_gone(rest, 15.0)
            log(f"   Server beendet nach {time.time() - t_stop:.0f}s, "
                f"MemAvailable {mem_available() / GIB:.1f} GiB")



if __name__ == "__main__":
    sys.exit(main())
