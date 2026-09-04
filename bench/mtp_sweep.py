#!/usr/bin/env python3
"""Sweep 2: MTP-Spekulation über den Server messen (tg t/s, Draft-Akzeptanz) – verschiedene n_max/p_min/temp.

Nutzung: uv run python bench/mtp_sweep.py [--quick]
Ergebnisse: bench/results/mtp/<name>.json + summary.jsonl
"""
from __future__ import annotations

import json, os, signal, subprocess, sys, time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "bench" / "results" / "mtp"
OUT.mkdir(parents=True, exist_ok=True)
BIN = ROOT / "engine" / "build-hip" / "bin" / "llama"
HF = Path.home() / ".cache/huggingface/hub"
M4 = HF / "models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/c8b5954a88c2775c546b92593eda40ea041d3176/UD-Q4_K_XL/Qwen3.8-Flash-Next-UD-Q4_K_XL-00001-of-00004.gguf"
M2 = HF / "models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-Q2_K_XL/Qwen3.8-Flash-Next-UD-Q2_K_XL-00001-of-00003.gguf"
MTP_DZ = HF / "models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf"
MTP_UN = HF / "models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/38bb39ee97821de2c9009abb7e93950eec396e66/MTP/mtp-Qwen3.8-Flash-Next-Q4_K_M.gguf"
PORT = 8099
BASE = f"http://127.0.0.1:{PORT}"

PROMPTS = [
    ("code", "Schreibe eine vollständige Python-Klasse `LRUCache` mit get/put in O(1), Typannotationen, Docstrings und 5 pytest-Tests."),
    ("prosa", "Erkläre einem Erstsemester in etwa 400 Wörtern, wie ein Mixture-of-Experts-Sprachmodell funktioniert und warum es schneller ist als ein dichtes Modell gleicher Größe."),
    ("reasoning", "Ein Zug fährt um 8:00 mit 80 km/h von A nach B (240 km). Ein zweiter Zug fährt um 8:30 mit 120 km/h von B nach A. Wann und wo treffen sie sich? Rechne Schritt für Schritt."),
]

BASE_ARGS = ["-ngl", "99", "-c", "32768", "-fa", "on", "-ctk", "q8_0", "-ctv", "q8_0", "-t", "16", "-b", "2048", "-ub", "512",
             "--tensor-read-lazy", "auto", "--jinja", "--chat-template-kwargs", '{"reasoning_effort":"medium"}',
             "--host", "127.0.0.1", "--port", str(PORT), "--no-webui", "-np", "1", "--top-p", "0.95", "--top-k", "20", "--min-p", "0"]


def mtp(head: Path, n_max: int, p_min: float, extra: list[str] | None = None) -> list[str]:
    return ["-md", str(head), "-ngld", "99", "--spec-type", "draft-mtp", "--spec-draft-n-max", str(n_max), "--spec-draft-p-min", str(p_min)] + (extra or [])


CONFIGS: list[tuple[str, Path, list[str]]] = [
    ("q4-nomtp-t1.0",            M4, ["--temp", "1.0"]),
    ("q4-mtp-dz-n3-p0.75-t1.0",  M4, ["--temp", "1.0"] + mtp(MTP_DZ, 3, 0.75)),
    ("q4-mtp-un-n3-p0.75-t1.0",  M4, ["--temp", "1.0"] + mtp(MTP_UN, 3, 0.75)),
    ("q4-mtp-dz-n3-p0.0-t1.0",   M4, ["--temp", "1.0"] + mtp(MTP_DZ, 3, 0.0)),
    ("q4-mtp-dz-n2-p0.75-t1.0",  M4, ["--temp", "1.0"] + mtp(MTP_DZ, 2, 0.75)),
    ("q4-mtp-dz-n4-p0.75-t1.0",  M4, ["--temp", "1.0"] + mtp(MTP_DZ, 4, 0.75)),
    ("q4-mtp-dz-n5-p0.5-t1.0",   M4, ["--temp", "1.0"] + mtp(MTP_DZ, 5, 0.5)),
    ("q4-mtp-dz-n3-p0.75-t0.6",  M4, ["--temp", "0.6"] + mtp(MTP_DZ, 3, 0.75)),
    ("q4-mtp-dz-n3-p0.75-ngram", M4, ["--temp", "1.0"] + mtp(MTP_DZ, 3, 0.75) + ["--spec-type", "draft-mtp,ngram-mod"]),
    ("q2-nomtp-t1.0",            M2, ["--temp", "1.0"]),
    ("q2-mtp-dz-n3-p0.75-t1.0",  M2, ["--temp", "1.0"] + mtp(MTP_DZ, 3, 0.75)),
]
if "--quick" in sys.argv:
    CONFIGS = CONFIGS[:2]


def wait_ready(proc: subprocess.Popen, timeout: float = 600) -> bool:
    t0 = time.time()
    while time.time() - t0 < timeout:
        if proc.poll() is not None:
            return False
        try:
            r = httpx.get(BASE + "/health", timeout=3)
            if r.status_code == 200 and r.json().get("status") == "ok":
                return True
        except Exception:
            pass
        time.sleep(2)
    return False


def run_prompt(prompt: str, max_tokens: int = 400) -> dict:
    body = {"messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens, "stream": False}
    t0 = time.time()
    r = httpx.post(BASE + "/v1/chat/completions", json=body, timeout=900)
    r.raise_for_status()
    d = r.json()
    t = d.get("timings", {})
    return {"wall": time.time() - t0, "timings": t, "finish": d["choices"][0].get("finish_reason"),
            "n_content": len(d["choices"][0]["message"].get("content") or ""), "n_reasoning": len(d["choices"][0]["message"].get("reasoning_content") or "")}


def main() -> None:
    summary = OUT / "summary.jsonl"
    for name, model, args in CONFIGS:
        if (OUT / f"{name}.json").exists() and "--force" not in sys.argv:
            print(f"### {name}: vorhanden, übersprungen"); continue
        argv = [str(BIN), "serve", "-m", str(model)] + BASE_ARGS + args
        env = dict(os.environ, LLAMA_ATTN_ROT_DISABLE="1")
        log = (OUT / f"{name}.log").open("w")
        log.write(" ".join(argv) + "\n")
        print(f"### {time.strftime('%H:%M:%S')} {name}")
        t0 = time.time()
        proc = subprocess.Popen(argv, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        res = {"name": name, "model": model.parent.name, "args": args, "runs": [], "error": ""}
        try:
            if not wait_ready(proc):
                res["error"] = "server nicht bereit"
                print("   FEHLER: Server nicht bereit (siehe Log)")
            else:
                res["load_s"] = time.time() - t0
                # Warmup (kurz), dann Messläufe
                run_prompt("Sag nur: bereit.", 16)
                for key, p in PROMPTS:
                    r = run_prompt(p)
                    r["prompt"] = key
                    res["runs"].append(r)
                    t = r["timings"]
                    dn, da = t.get("draft_n", 0), t.get("draft_n_accepted", 0)
                    acc = f" draft {da}/{dn} = {da / dn:.0%}" if dn else ""
                    print(f"   {key:10} pp {t.get('prompt_per_second', 0):6.1f} t/s | tg {t.get('predicted_per_second', 0):6.2f} t/s | n={t.get('predicted_n')} {r['finish']}{acc}")
        except Exception as e:
            res["error"] = f"{e.__class__.__name__}: {e}"
            print("   FEHLER:", res["error"])
        finally:
            try:
                os.killpg(proc.pid, signal.SIGINT)
                proc.wait(timeout=60)
            except Exception:
                os.killpg(proc.pid, signal.SIGKILL)
            log.close()
        if res["runs"]:
            tg = [r["timings"].get("predicted_per_second", 0) for r in res["runs"]]
            res["tg_mean"] = sum(tg) / len(tg)
            dn = sum(r["timings"].get("draft_n", 0) for r in res["runs"])
            da = sum(r["timings"].get("draft_n_accepted", 0) for r in res["runs"])
            res["accept"] = da / dn if dn else None
            print(f"   => tg Ø {res['tg_mean']:.2f} t/s" + (f", Akzeptanz {res['accept']:.0%}" if dn else "") + f", Load {res.get('load_s', 0):.0f}s")
        (OUT / f"{name}.json").write_text(json.dumps(res, indent=1))
        with summary.open("a") as f:
            f.write(json.dumps({k: res.get(k) for k in ("name", "model", "tg_mean", "accept", "load_s", "error")}) + "\n")
        time.sleep(3)
    print("### fertig", time.strftime("%H:%M:%S"))


if __name__ == "__main__":
    main()
