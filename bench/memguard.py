#!/usr/bin/env python3
"""Speicher-Wächter: startet ein Kommando in einer eigenen Prozessgruppe und killt es hart (SIGKILL),
sobald MemAvailable unter eine Schwelle fällt – bevor der Kernel-OOM-Killer zuschlägt.
Zeichnet MemAvailable, GTT/VRAM-Belegung und RSS des Prozesses als CSV auf.

  memguard.py [--min-avail-gib 10] [--csv datei] [--stop-after-ready-cmd 'python ...'] -- CMD ARGS...
Exit 137 = vom Wächter abgebrochen.
"""
from __future__ import annotations

import argparse, os, signal, subprocess, sys, time
from pathlib import Path

GIB = 2**30


def meminfo() -> dict[str, int]:
    out = {}
    with open("/proc/meminfo") as f:
        for line in f:
            k, v = line.split(":", 1)
            out[k] = int(v.split()[0]) * 1024
    return out


def gpu_mem() -> tuple[int, int]:
    def rd(p):
        try:
            return int(Path(p).read_text())
        except Exception:
            return 0
    return rd("/sys/class/drm/card0/device/mem_info_gtt_used"), rd("/sys/class/drm/card0/device/mem_info_vram_used")


def rss(pid: int) -> int:
    try:
        for line in open(f"/proc/{pid}/status"):
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) * 1024
    except Exception:
        pass
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-avail-gib", type=float, default=10.0)
    ap.add_argument("--csv", default="")
    ap.add_argument("--interval", type=float, default=0.25)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    if not cmd:
        ap.error("Kommando fehlt")
    thr = int(a.min_avail_gib * GIB)
    csv = open(a.csv, "w") if a.csv else None
    if csv:
        csv.write("t,mem_available_gib,gtt_used_gib,vram_used_gib,rss_gib\n")
    base = meminfo()["MemAvailable"]
    proc = subprocess.Popen(cmd, start_new_session=True)
    t0 = time.time()
    min_avail, peak_gtt, peak_rss = base, 0, 0
    killed = False
    try:
        while proc.poll() is None:
            mi = meminfo()
            avail = mi["MemAvailable"]
            gtt, vram = gpu_mem()
            r = rss(proc.pid)
            min_avail, peak_gtt, peak_rss = min(min_avail, avail), max(peak_gtt, gtt), max(peak_rss, r)
            if csv:
                csv.write(f"{time.time() - t0:.2f},{avail / GIB:.2f},{gtt / GIB:.2f},{vram / GIB:.2f},{r / GIB:.2f}\n")
                csv.flush()
            if avail < thr:
                print(f"[memguard] MemAvailable {avail / GIB:.1f} GiB < {thr / GIB:.1f} GiB -> SIGKILL Prozessgruppe {proc.pid}", file=sys.stderr, flush=True)
                os.killpg(proc.pid, signal.SIGKILL)
                killed = True
                break
            time.sleep(a.interval)
    except KeyboardInterrupt:
        os.killpg(proc.pid, signal.SIGINT)
    proc.wait()
    print(f"[memguard] fertig nach {time.time() - t0:.0f}s: MemAvailable Start {base / GIB:.1f} GiB, Minimum {min_avail / GIB:.1f} GiB "
          f"(Verbrauch {(base - min_avail) / GIB:.1f} GiB), Peak GTT {peak_gtt / GIB:.1f} GiB, Peak RSS {peak_rss / GIB:.1f} GiB, "
          f"exit {proc.returncode}{' KILLED' if killed else ''}", file=sys.stderr, flush=True)
    if csv:
        csv.close()
    return 137 if killed else (proc.returncode or 0)


if __name__ == "__main__":
    sys.exit(main())
