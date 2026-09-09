#!/usr/bin/env python3
"""Cache-Verhalten bei agentischen Lasten messen.

Simuliert mehrere Agenten-Sitzungen, die abwechselnd weiterlaufen: jede Sitzung beginnt mit einem
langen Dokument und stellt danach Runde für Runde kurze Anschlussfragen. Genau das macht ein Agent,
und genau da entscheidet sich, ob der Server den Prompt jedes Mal neu verarbeitet oder aus dem Cache
holt. Der Server meldet je Antwort `cache_n` (aus dem Cache) und `prompt_n` (neu verarbeitet); die
Sonde rechnet daraus die Trefferquote je Runde aus.

Mehr Sitzungen als Slots erzwingen Verdrängung – dann zeigt sich, ob der RAM-Prompt-Cache
(--cache-ram) den verdrängten Zustand zurückholt oder ob alles neu gerechnet wird.

  bench/cache_probe.py --sessions 4 --turns 3 --slots 2 --prefix-tokens 8000

Der Server läuft unter bench/memguard.py.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
OUT = ROOT / "bench" / "results" / "cache"
GIB = 2**30
PORT = 8097
BASE = f"http://127.0.0.1:{PORT}"

# Füllmaterial mit sichtbarer Struktur: der Agent soll darauf verweisen können, und jede Sitzung
# bekommt ihr eigenes, damit die Präfixe sich nicht überschneiden.
ABSATZ = (
    "Abschnitt {i} des Moduls {tag}. Diese Funktion prüft die Eingabe, normalisiert die Pfade und "
    "schreibt das Ergebnis in den Zwischenspeicher. Bei einem Fehler wird die Ausnahme protokolliert "
    "und der Vorgang mit dem Statuscode {code} abgebrochen. Die Aufrufer verlassen sich darauf, dass "
    "der Rückgabewert niemals leer ist, und behandeln den Sonderfall {i} gesondert.\n"
)


def dokument(tag: str, ziel_tokens: int) -> str:
    """Ungefähr ziel_tokens Token Fülltext (grob 3 Token je 10 Zeichen bei diesem Tokenizer)."""
    teile, i = [], 0
    while sum(len(t) for t in teile) < ziel_tokens * 3.4:
        i += 1
        teile.append(ABSATZ.format(i=i, tag=tag, code=400 + (i % 90)))
    return "".join(teile)


def frei(port: int) -> bool:
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def server_argv(a) -> tuple[list[str], dict, object]:
    from qwen38tui.config import build_command
    from qwen38tui.discovery import discover_all
    from qwen38tui.hardware import probe
    from qwen38tui.presets import get_preset

    inv, hw = discover_all(), probe()
    cfg = get_preset(a.preset).apply().copy(
        quant=a.quant,
        n_parallel=a.slots,
        ctx_size=a.ctx_per_slot * a.slots,
        mtp_enabled=not a.no_mtp,
        cache_ram_mib=a.cache_ram,
        n_ctx_checkpoints=a.ctx_checkpoints,
        checkpoint_min_step=a.checkpoint_min_step,
        kv_unified=a.kv_unified,
        kv_unified_per_slot=a.kv_unified_per_slot,
    )
    cmd = build_command(cfg, inv, hw)
    if cmd.errors:
        print("\n".join("FEHLER: " + e for e in cmd.errors), file=sys.stderr, flush=True)
        raise SystemExit(2)
    from qwen38tui.memory import estimate
    r = cmd.resolved
    est = estimate(cfg, r.model, r.mtp, hw, "hip", True)
    return cmd.argv, cmd.env, est


def lauf(a) -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    if not frei(PORT):
        print(f"Port {PORT} belegt – läuft noch ein Server?", file=sys.stderr, flush=True)
        return 2
    argv, env, est = server_argv(a)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    logpfad = OUT / f"{a.tag}-{stamp}.log"
    voll = [sys.executable, str(ROOT / "bench" / "memguard.py"),
            "--min-avail-gib", str(a.min_avail), "--"] + argv + [
            "--host", "127.0.0.1", "--port", str(PORT), "--no-webui", "-lv", "5"]
    log = logpfad.open("w")
    log.write(" ".join(voll) + "\n\n")
    log.flush()
    umgebung = dict(os.environ)
    umgebung.update(env)
    print(f"Schätzung: {est.total / GIB:.1f} GiB belegt, {est.headroom / GIB:.1f} GiB Spielraum", flush=True)
    print(f"Start: {a.slots} Slots à {a.ctx_per_slot} Token, cache-ram {a.cache_ram} MiB, "
          f"ctx-checkpoints {a.ctx_checkpoints}", flush=True)
    t0 = time.time()
    proc = subprocess.Popen(voll, env=umgebung, stdout=log, stderr=subprocess.STDOUT,
                            start_new_session=True)
    ergebnis = {"tag": a.tag, "argv": argv, "slots": a.slots, "ctx_per_slot": a.ctx_per_slot,
                "cache_ram_mib": a.cache_ram, "ctx_checkpoints": a.ctx_checkpoints,
                "checkpoint_min_step": a.checkpoint_min_step,
                "diverge_at": a.diverge_at,
                "sessions": a.sessions, "turns": a.turns, "prefix_tokens": a.prefix_tokens,
                "schaetzung_gib": round(est.total / GIB, 1), "runden": []}
    try:
        bereit = False
        while proc.poll() is None and time.time() - t0 < a.ready_timeout:
            try:
                r = httpx.get(BASE + "/health", timeout=2)
                if r.status_code == 200 and r.json().get("status") == "ok":
                    bereit = True
                    break
            except Exception:
                pass
            time.sleep(2)
        if not bereit:
            ergebnis["fehler"] = "Server nicht bereit"
            print("Server nicht bereit", file=sys.stderr, flush=True)
            return 1
        ergebnis["ladezeit_s"] = round(time.time() - t0, 1)
        print(f"bereit nach {ergebnis['ladezeit_s']:.0f}s\n", flush=True)
        verlauf = {s: [{"role": "user", "content": dokument(f"S{s}", a.prefix_tokens)
                        + f"\n\nFasse Abschnitt 3 aus Modul S{s} in einem Satz zusammen."}]
                   for s in range(a.sessions)}
        # Runde für Runde reihum: so wird jeder Slot zwischendurch für eine andere Sitzung gebraucht.
        for runde in range(a.turns):
            if runde == a.diverge_at:
                # Der Agent schreibt die Mitte seines Verlaufs um (Kompaktierung, Korrektur eines
                # Werkzeug-Ergebnisses). Ab dieser Stelle stimmt der Cache nicht mehr: ohne
                # Checkpoint muss der Server ab Token 0 rechnen, mit Checkpoint ab dem letzten davor.
                for s in range(a.sessions):
                    erst = verlauf[s][0]["content"]
                    mitte = len(erst) // 2
                    schnitt = erst.find("Abschnitt ", mitte)
                    if schnitt > 0:
                        verlauf[s][0]["content"] = (
                            erst[:schnitt] + "Ersetzter Abschnitt: dieser Teil wurde zusammengefasst. "
                            + erst[schnitt:])
                print(f"  -- Runde {runde}: Verlaufsmitte umgeschrieben (Divergenz)", flush=True)
            for s in range(a.sessions):
                t1 = time.time()
                try:
                    antwort = httpx.post(BASE + "/v1/chat/completions", json={
                        "messages": verlauf[s], "max_tokens": a.max_tokens, "stream": False,
                        "temperature": 0.7,
                    }, timeout=a.request_timeout).json()
                except Exception as e:
                    ergebnis.setdefault("fehler_anfragen", []).append(repr(e))
                    print(f"  Runde {runde} Sitzung {s}: Fehler {e!r}", flush=True)
                    continue
                dauer = time.time() - t1
                if "choices" not in antwort:
                    # Der Server lehnt ab, z. B. wenn der Prompt länger ist als der Kontext des Slots.
                    meldung = (antwort.get("error") or {}).get("message") or json.dumps(antwort)[:300]
                    ergebnis.setdefault("abgelehnt", []).append(
                        {"runde": runde, "sitzung": s, "meldung": meldung})
                    print(f"  Runde {runde} Sitzung {s}: abgelehnt – {meldung}", flush=True)
                    continue
                t = antwort.get("timings", {})
                text = antwort["choices"][0]["message"].get("content") or ""
                cache_n, prompt_n = t.get("cache_n", 0), t.get("prompt_n", 0)
                gesamt = cache_n + prompt_n
                zeile = {
                    "runde": runde, "sitzung": s, "prompt_gesamt": gesamt, "cache_n": cache_n,
                    "prompt_n": prompt_n,
                    "trefferquote": round(cache_n / gesamt, 3) if gesamt else 0.0,
                    "pp_t_s": round(t.get("prompt_per_second") or 0, 1),
                    "tg_t_s": round(t.get("predicted_per_second") or 0, 1),
                    "dauer_s": round(dauer, 1),
                    "ausgabe_tokens": t.get("predicted_n"),
                }
                ergebnis["runden"].append(zeile)
                print(f"  Runde {runde} Sitzung {s}: Prompt {gesamt:>7} Token, davon {cache_n:>7} "
                      f"aus dem Cache ({zeile['trefferquote']*100:4.1f} %), neu {prompt_n:>6}, "
                      f"{dauer:5.1f}s, {zeile['tg_t_s']:.1f} t/s", flush=True)
                verlauf[s].append({"role": "assistant", "content": text})
                verlauf[s].append({"role": "user", "content":
                                   f"Runde {runde + 2}: Nenne einen weiteren Aspekt in einem Satz."})
    finally:
        for pid in subprocess.run(["pgrep", "-x", "llama"], capture_output=True,
                                  text=True).stdout.split():
            try:
                os.kill(int(pid), signal.SIGKILL)
            except Exception:
                pass
        try:
            proc.wait(timeout=60)
        except subprocess.TimeoutExpired:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            proc.wait()
        log.close()
    text = logpfad.read_text(errors="replace")
    groessen = [float(m) for m in re.findall(r"created context checkpoint.*?size = ([0-9.]+) MiB", text)]
    if groessen:
        ergebnis["checkpoint_mib"] = round(sum(groessen) / len(groessen), 1)
        ergebnis["checkpoints_erzeugt"] = len(groessen)
    ergebnis["checkpoints_verworfen"] = len(re.findall(r"erasing old context checkpoint", text))
    ergebnis["cache_meldungen"] = sorted(set(re.findall(
        r"(prompt cache[^\n]*|- cache state[^\n]*|restored[^\n]*from the cache[^\n]*)", text)))[:12]
    ergebnis["guard"] = next((l for l in reversed(text.splitlines()) if "[memguard] fertig" in l), "")
    (OUT / f"{a.tag}-{stamp}.json").write_text(json.dumps(ergebnis, indent=1, ensure_ascii=False))
    quoten = [z["trefferquote"] for z in ergebnis["runden"] if z["runde"] > 0]
    print(f"\nTrefferquote ab Runde 2: Ø {sum(quoten)/len(quoten)*100:.1f} %"
          if quoten else "\nkeine Folgerunden gemessen")
    if groessen:
        print(f"Context-Checkpoints: {len(groessen)} erzeugt, je Ø {ergebnis['checkpoint_mib']:.1f} MiB", flush=True)
    print(f"Log: {logpfad}\nJSON: {OUT / f'{a.tag}-{stamp}.json'}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tag", default="cache")
    ap.add_argument("--preset", default="eh-agent")
    ap.add_argument("--quant", default="UD-IQ3_XXS")
    ap.add_argument("--slots", type=int, default=2)
    ap.add_argument("--ctx-per-slot", type=int, default=32768)
    ap.add_argument("--cache-ram", type=int, default=8192, help="MiB, -1 unbegrenzt, 0 aus")
    ap.add_argument("--ctx-checkpoints", type=int, default=32)
    ap.add_argument("--checkpoint-min-step", type=int, default=8192)
    ap.add_argument("--kv-unified", default="auto", choices=("auto", "on", "off"))
    ap.add_argument("--kv-unified-per-slot", type=int, default=0)
    ap.add_argument("--no-mtp", action="store_true")
    ap.add_argument("--sessions", type=int, default=4)
    ap.add_argument("--turns", type=int, default=3)
    ap.add_argument("--prefix-tokens", type=int, default=8000)
    ap.add_argument("--diverge-at", type=int, default=-1,
                    help="in dieser Runde die Mitte des Verlaufs umschreiben (-1 = nie)")
    ap.add_argument("--max-tokens", type=int, default=120)
    ap.add_argument("--request-timeout", type=float, default=1800)
    ap.add_argument("--ready-timeout", type=float, default=900)
    ap.add_argument("--min-avail", type=float, default=8)
    return lauf(ap.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
