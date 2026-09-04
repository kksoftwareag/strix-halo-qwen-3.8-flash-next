#!/usr/bin/env python3
"""Sweep 7: MTP-Feintuning über den Server (unter memguard) – n_max / p_min / temp / ngram-mod, je Engine+Quant.

  uv run python bench/mtp_sweep2.py --engine engramhalo|own --quant IQ3_XXS|IQ4_XS|Q2_K_XL [--lm none|mmap|auto] [--quick]
Ergebnisse: bench/results/mtp2/<engine>-<quant>-<name>.json + summary.jsonl
"""
from __future__ import annotations
import argparse, json, os, signal, subprocess, sys, time
from pathlib import Path
import httpx

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "bench" / "results" / "mtp2"; OUT.mkdir(parents=True, exist_ok=True)
HF = Path.home() / ".cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots"
MODELS = {
    "Q2_K_XL": HF / "824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-Q2_K_XL/Qwen3.8-Flash-Next-UD-Q2_K_XL-00001-of-00003.gguf",
    "IQ3_XXS": HF / "824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-IQ3_XXS/Qwen3.8-Flash-Next-UD-IQ3_XXS-00001-of-00003.gguf",
    "IQ4_XS": HF / "824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-IQ4_XS/Qwen3.8-Flash-Next-UD-IQ4_XS-00001-of-00003.gguf",
    "Q4_K_XL": HF / "c8b5954a88c2775c546b92593eda40ea041d3176/UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf",
}
MTP = Path.home() / ".cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf"
ENGINES = {"engramhalo": ROOT / "engine/build-engramhalo/bin/llama", "own": ROOT / "engine/build-hip/bin/llama"}
PORT = 8097; BASE = f"http://127.0.0.1:{PORT}"
PROMPTS = [
    ("code", "Schreibe eine vollständige Python-Klasse `LRUCache` mit get/put in O(1), Typannotationen, Docstrings und 5 pytest-Tests."),
    ("prosa", "Erkläre einem Erstsemester in etwa 400 Wörtern, wie ein Mixture-of-Experts-Sprachmodell funktioniert und warum es schneller ist als ein dichtes Modell gleicher Größe."),
    ("reasoning", "Ein Zug fährt um 8:00 mit 80 km/h von A nach B (240 km). Ein zweiter Zug fährt um 8:30 mit 120 km/h von B nach A. Wann und wo treffen sie sich? Rechne Schritt für Schritt."),
]


def mtp(n_max, p_min, ngram=False):
    return ["-md", str(MTP), "-ngld", "99", "--spec-type", "draft-mtp" + (",ngram-mod" if ngram else ""), "--spec-draft-n-max", str(n_max), "--spec-draft-p-min", str(p_min)]


def configs(quick: bool):
    c = [
        ("nomtp-t1.0",        ["--temp", "1.0"]),
        ("n3-p0.75-t1.0",     ["--temp", "1.0"] + mtp(3, 0.75)),
        ("n4-p0.75-ng-t1.0",  ["--temp", "1.0"] + mtp(4, 0.75, True)),
        ("n2-p0.75-t1.0",     ["--temp", "1.0"] + mtp(2, 0.75)),
        ("n4-p0.0-t1.0",      ["--temp", "1.0"] + mtp(4, 0.0)),
        ("n3-p0.75-t0.6",     ["--temp", "0.6"] + mtp(3, 0.75)),
        ("n3-p0.75-t0.0",     ["--temp", "0.0"] + mtp(3, 0.75)),
        ("n6-p0.75-ng-t1.0",  ["--temp", "1.0"] + mtp(6, 0.75, True)),
    ]
    return c[:3] if quick else c


def wait_ready(proc, timeout):
    t0 = time.time()
    while time.time() - t0 < timeout and proc.poll() is None:
        try:
            r = httpx.get(BASE + "/health", timeout=3)
            if r.status_code == 200 and r.json().get("status") == "ok":
                return True
        except Exception:
            pass
        time.sleep(2)
    return False


def kill_llama():
    try:
        for pid in subprocess.check_output(["pgrep", "-x", "llama"]).split():
            os.kill(int(pid), signal.SIGKILL)
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default="engramhalo", choices=ENGINES)
    ap.add_argument("--quant", default="IQ3_XXS", choices=MODELS)
    ap.add_argument("--lm", default="none")
    ap.add_argument("--ctx", type=int, default=32768)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    import socket
    with socket.socket() as s:
        if s.connect_ex(("127.0.0.1", PORT)) == 0:
            print("Port belegt"); sys.exit(2)
    bin_ = ENGINES[a.engine]
    eh = a.engine == "engramhalo"
    base = ["-ngl", "999", "-c", str(a.ctx), "-fa", "on", "-ctk", "q8_0", "-ctv", "q8_0", "--jinja", "--chat-template-kwargs", '{"reasoning_effort":"medium"}',
            "--host", "127.0.0.1", "--port", str(PORT), "--no-webui", "-np", "1", "--top-p", "0.95", "--top-k", "20", "--min-p", "0", "-lv", "3"]
    base += (["-b", "8192", "-ub", "2048", "-t", "4"] if eh else ["-b", "2048", "-ub", "512", "-t", "16"])
    if a.lm != "auto":
        base += ["-lm", a.lm]
        if a.lm == "mmap":
            base += ["--tensor-read-lazy", "on"]
    env = dict(os.environ)
    if eh:
        env["ROCBLAS_USE_HIPBLASLT"] = "1"
    summary = OUT / "summary.jsonl"
    for name, args in configs(a.quick):
        tag = f"{a.engine}-{a.quant}-{a.lm}-{name}"
        if (OUT / f"{tag}.json").exists() and not a.force:
            print(f"### {tag}: vorhanden"); continue
        argv = [sys.executable, str(ROOT / "bench/memguard.py"), "--min-avail-gib", "8", "--csv", str(OUT / f"{tag}.csv"), "--",
                str(bin_), "serve", "-m", str(MODELS[a.quant])] + base + args
        log = (OUT / f"{tag}.log").open("w"); log.write(" ".join(argv) + "\n"); log.flush()
        print(f"### {time.strftime('%H:%M:%S')} {tag}", flush=True)
        t0 = time.time()
        proc = subprocess.Popen(argv, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        res = {"tag": tag, "engine": a.engine, "quant": a.quant, "lm": a.lm, "name": name, "args": args, "runs": [], "error": ""}
        try:
            if not wait_ready(proc, 1500):
                res["error"] = "nicht bereit"; print("   FEHLER: nicht bereit")
            else:
                res["load_s"] = time.time() - t0
                httpx.post(BASE + "/v1/chat/completions", json={"messages": [{"role": "user", "content": "Sag nur: bereit."}], "max_tokens": 16}, timeout=600)
                for key, p in PROMPTS:
                    tq = time.time()
                    r = httpx.post(BASE + "/v1/chat/completions", json={"messages": [{"role": "user", "content": p}], "max_tokens": 400, "stream": False}, timeout=900).json()
                    t = r.get("timings", {})
                    res["runs"].append({"prompt": key, "wall": time.time() - tq, **t})
                    dn, da = t.get("draft_n", 0), t.get("draft_n_accepted", 0)
                    print(f"   {key:10} pp {t.get('prompt_per_second', 0):6.1f} | tg {t.get('predicted_per_second', 0):6.2f} t/s | n={t.get('predicted_n')}" + (f" | draft {da}/{dn} = {da / dn:.0%}" if dn else ""), flush=True)
        except Exception as e:
            res["error"] = f"{e.__class__.__name__}: {e}"; print("   FEHLER:", res["error"])
        finally:
            kill_llama()
            try:
                proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL); proc.wait()
            log.close()
        if res["runs"]:
            tg = [x.get("predicted_per_second", 0) for x in res["runs"]]
            res["tg_mean"] = sum(tg) / len(tg)
            res["tg_code"] = next((x.get("predicted_per_second") for x in res["runs"] if x["prompt"] == "code"), None)
            dn = sum(x.get("draft_n", 0) for x in res["runs"]); da = sum(x.get("draft_n_accepted", 0) for x in res["runs"])
            res["accept"] = da / dn if dn else None
            print(f"   => tg Ø {res['tg_mean']:.2f} t/s (code {res['tg_code']:.2f})" + (f", Akzeptanz {res['accept']:.0%}" if dn else "") + f", Load {res.get('load_s', 0):.0f}s", flush=True)
        (OUT / f"{tag}.json").write_text(json.dumps(res, indent=1))
        with summary.open("a") as f:
            f.write(json.dumps({k: res.get(k) for k in ("tag", "engine", "quant", "lm", "name", "tg_mean", "tg_code", "accept", "load_s", "error")}) + "\n")
        time.sleep(3)
    print("### fertig", time.strftime("%H:%M:%S"))


if __name__ == "__main__":
    main()
