#!/usr/bin/env python3
"""Footprint-Messung: Server starten (unter memguard), eine Anfrage, stoppen. Meldet Peak-Verbrauch.
   uv run python bench/mem_probe.py <name> -- <llama serve args...>
"""
from __future__ import annotations
import json, os, signal, subprocess, sys, time
from pathlib import Path
import httpx

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "bench" / "results" / "mem"
OUT.mkdir(parents=True, exist_ok=True)
name = sys.argv[1]
args = sys.argv[3:] if sys.argv[2] == "--" else sys.argv[2:]
PORT = 8098
BASE = f"http://127.0.0.1:{PORT}"
import socket
with socket.socket() as _s:  # Port-Check: fremder Server wuerde /health faelschlich beantworten
    if _s.connect_ex(("127.0.0.1", PORT)) == 0:
        print(json.dumps({"name": name, "error": f"Port {PORT} belegt - fremder Server laeuft noch"})); sys.exit(2)
argv = [sys.executable, str(ROOT / "bench" / "memguard.py"), "--min-avail-gib", os.environ.get("MIN_AVAIL_GIB", "10"), "--csv", str(OUT / f"{name}.csv"), "--"] + args + ["--host", "127.0.0.1", "--port", str(PORT), "--no-webui"]
log = (OUT / f"{name}.log").open("w")
log.write(" ".join(argv) + "\n"); log.flush()
env = dict(os.environ)
for kv in [x for x in os.environ.get("PROBE_ENV", "").split(",") if "=" in x]:
    k, v = kv.split("=", 1); env[k] = v
res_env = {k: env[k] for k in ("LLAMA_ATTN_ROT_DISABLE", "ROCBLAS_USE_HIPBLASLT", "LLAMA_QSA_GATHER", "GGML_HIP_GDN_CHUNK", "LLAMA_MMAP_DROP_BEHIND") if k in env}
t0 = time.time()
proc = subprocess.Popen(argv, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)  # eigene Gruppe: killpg trifft nie das Sweep-Skript
res = {"name": name, "args": args, "env": res_env}
ready = False
while proc.poll() is None and time.time() - t0 < float(os.environ.get("READY_TIMEOUT", "900")):
    try:
        r = httpx.get(BASE + "/health", timeout=2)
        if r.status_code == 200 and r.json().get("status") == "ok":
            ready = True; break
    except Exception:
        pass
    time.sleep(1)
if ready:
    res["load_s"] = time.time() - t0
    try:
        r = httpx.post(BASE + "/v1/chat/completions", json={"messages": [{"role": "user", "content": "Zähle von 1 bis 30 und erkläre danach in 5 Sätzen, was ein KV-Cache ist."}], "max_tokens": 300, "stream": False}, timeout=600).json()
        t = r.get("timings", {})
        res["tg"] = t.get("predicted_per_second"); res["pp"] = t.get("prompt_per_second"); res["draft_n"] = t.get("draft_n"); res["draft_acc"] = t.get("draft_n_accepted")
    except Exception as e:
        res["req_error"] = repr(e)
    time.sleep(2)
else:
    res["error"] = "Server nicht bereit (Timeout/Abbruch)"
# Server hart beenden (SIGKILL gibt GTT sofort frei; ein sauberer Shutdown dauert bei 50-80 GiB Minuten)
def _kill_llama(sig):
    try:
        for pid in subprocess.check_output(["pgrep", "-x", "llama"]).split():
            os.kill(int(pid), sig)
    except Exception:
        pass
_kill_llama(signal.SIGKILL)
try:
    proc.wait(timeout=60)
except subprocess.TimeoutExpired:
    os.killpg(os.getpgid(proc.pid), signal.SIGKILL); proc.wait()
res["guard_exit"] = proc.returncode
log.close()
tail = (OUT / f"{name}.log").read_text().splitlines()
res["guard_summary"] = next((l for l in reversed(tail) if "[memguard] fertig" in l), "")
(OUT / f"{name}.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, ensure_ascii=False))
