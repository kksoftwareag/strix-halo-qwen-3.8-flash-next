#!/usr/bin/env python3
"""Kleiner Benchmark gegen einen bereits laufenden Server (z. B. den systemd-Dienst).

`bench-parallel` startet für jede Messung einen eigenen Server. Diese Sonde tut das nicht: sie fragt
den Dienst, der ohnehin läuft, und misst dabei genau das, was Nutzer sehen – Zeit bis zum ersten
Token, Dekodierrate, Draft-Akzeptanz. Jede Anfrage bekommt ein eigenes Codewort, das in der Antwort
wieder auftauchen muss; so fällt auf, wenn bei mehreren Slots die Ausgabe kaputtgeht (Issue #27572).

  bench/live_bench.py --levels 1,2,4 --max-tokens 300
  bench/live_bench.py --url http://10.50.4.9:8080 --key-file state/api-keys.txt
"""
from __future__ import annotations

import argparse
import asyncio
import statistics
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
WOERTER = ["Kobalt", "Zeder", "Malachit", "Fjord", "Zenit", "Onyx", "Lawine", "Quarz"]


def schluessel(a) -> str:
    if a.key:
        return a.key
    p = Path(a.key_file if Path(a.key_file).is_absolute() else ROOT / a.key_file)
    for zeile in p.read_text().splitlines():
        zeile = zeile.strip()
        if zeile and not zeile.startswith("#"):
            return zeile
    raise SystemExit(f"Kein Schlüssel in {p}")


async def eine_anfrage(client: httpx.AsyncClient, url: str, kopf: dict, i: int, a) -> dict:
    wort = WOERTER[i % len(WOERTER)]
    inhalt = (f"Das Codewort lautet {wort}. Erkläre in etwa {a.max_tokens // 3} Wörtern, wie ein "
              f"KV-Cache in einem Transformer funktioniert, und nenne am Ende das Codewort.")
    t0 = time.time()
    erste = None
    ende = ""
    text = []
    daten = {"messages": [{"role": "user", "content": inhalt}], "max_tokens": a.max_tokens,
             "stream": True, "stream_options": {"include_usage": True}, "temperature": 0.7}
    timings = {}
    async with client.stream("POST", f"{url}/v1/chat/completions", json=daten,
                             headers=kopf, timeout=a.timeout) as r:
        r.raise_for_status()
        async for zeile in r.aiter_lines():
            if not zeile.startswith("data: "):
                continue
            nutz = zeile[6:]
            if nutz.strip() == "[DONE]":
                break
            import json as _j
            try:
                stueck = _j.loads(nutz)
            except Exception:
                continue
            if stueck.get("timings"):
                timings = stueck["timings"]
            for w in stueck.get("choices", []):
                if w.get("finish_reason"):
                    ende = w["finish_reason"]
                delta = w.get("delta") or {}
                # Beim Thinking-Modell kommt zuerst reasoning_content; für die Zeit bis zum ersten
                # Token zählt beides, für den Codewort-Test nur die eigentliche Antwort.
                if delta.get("reasoning_content") and erste is None:
                    erste = time.time() - t0
                d = delta.get("content")
                if d:
                    if erste is None:
                        erste = time.time() - t0
                    text.append(d)
    ganz = "".join(text)
    return {"ttft": erste or (time.time() - t0), "dauer": time.time() - t0,
            "tg": timings.get("predicted_per_second"), "n": timings.get("predicted_n"),
            "draft_n": timings.get("draft_n"), "draft_ok": timings.get("draft_n_accepted"),
            # Nur eine vollständig zu Ende gelaufene Antwort kann das Codewort enthalten; wer ins
            # Token-Limit läuft, ist abgeschnitten und beweist nichts über die Ausgabequalität.
            "vollstaendig": ende == "stop",
            "wort_ok": ende != "stop" or wort.lower() in ganz.lower()}


async def stufe(url: str, kopf: dict, n: int, a) -> dict:
    async with httpx.AsyncClient() as client:
        t0 = time.time()
        ergebnisse = await asyncio.gather(*[eine_anfrage(client, url, kopf, i, a) for i in range(n)])
        gesamt = time.time() - t0
    tokens = sum(r["n"] or 0 for r in ergebnisse)
    draft_n = sum(r["draft_n"] or 0 for r in ergebnisse)
    draft_ok = sum(r["draft_ok"] or 0 for r in ergebnisse)
    return {
        "n": n, "summe_ts": tokens / gesamt if gesamt else 0,
        "je_nutzer": statistics.mean([r["tg"] or 0 for r in ergebnisse]),
        "min_ts": min(r["tg"] or 0 for r in ergebnisse),
        "ttft": statistics.median([r["ttft"] for r in ergebnisse]),
        "akzeptanz": draft_ok / draft_n if draft_n else 0.0,
        "fehlwort": sum(0 if r["wort_ok"] else 1 for r in ergebnisse),
        "abgeschnitten": sum(0 if r["vollstaendig"] else 1 for r in ergebnisse), "tokens": tokens,
    }


async def lauf(a) -> int:
    url = a.url.rstrip("/")
    kopf = {"Authorization": f"Bearer {schluessel(a)}"}
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{url}/health", headers=kopf, timeout=10)
        if r.status_code != 200:
            print(f"Server antwortet mit HTTP {r.status_code} auf /health", file=sys.stderr)
            return 1
    stufen = [int(x) for x in a.levels.split(",") if x.strip()]
    print(f"# {url}, max_tokens {a.max_tokens}, temp 0.7\n# Σ t/s zählt alle erzeugten Token (Denken eingeschlossen), TTFT die Zeit bis zum ersten davon.")
    if a.warmup:
        await stufe(url, kopf, 1, a)   # erste Anfrage füllt Caches, zählt nicht mit
    print(f"{'Nutzer':>6} {'Σ t/s':>8} {'je Nutzer':>10} {'min':>7} {'TTFT':>7} "
          f"{'Draft':>7} {'Tokens':>7} {'Codewort':>9}")
    for n in stufen:
        e = await stufe(url, kopf, n, a)
        print(f"{e['n']:>6} {e['summe_ts']:>8.1f} {e['je_nutzer']:>10.1f} {e['min_ts']:>7.1f} "
              f"{e['ttft']:>6.2f}s {e['akzeptanz']:>7.2f} {e['tokens']:>7} "
              f"{('ok' if not e['fehlwort'] else str(e['fehlwort']) + ' fehlen'):>9}"
              f"{('  ' + str(e['abgeschnitten']) + ' abgeschnitten') if e['abgeschnitten'] else ''}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default="http://127.0.0.1:8080")
    ap.add_argument("--key", default="")
    ap.add_argument("--key-file", default="state/api-keys.txt")
    ap.add_argument("--levels", default="1,2,4")
    ap.add_argument("--max-tokens", type=int, default=800,
                    help="im Thinking-Modus geht ein Teil davon für das Denken drauf")
    ap.add_argument("--timeout", type=float, default=600)
    ap.add_argument("--no-warmup", dest="warmup", action="store_false")
    return asyncio.run(lauf(ap.parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
