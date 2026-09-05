#!/usr/bin/env python3
"""Mehrnutzer-Messreihen aus state/bench/results.jsonl auswerten.

Trennt zwei Dinge, die der Benchmark beide als „Mix-up" zählt:
  * echtes Übersprechen – die Antwort enthält das Codewort eines anderen Nutzers
  * kaputte Ausgabe     – das eigene Codewort fehlt, ist verfälscht, oder die Antwort ist leer

Das zweite ist die Signatur des Fehlers aus llama.cpp-Issue #27572: Bei mehreren Slots und langen
Prompts landet Müll im Kontext, die Antworten werden leer oder falsch.

  bench/analyze_multiuser.py [--since 2026-09-05T21:00] [--markdown]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULTS = PROJECT / "state" / "bench" / "results.jsonl"


def classify(user: dict, codes: list[str]) -> str:
    """'ok' | 'uebersprechen' | 'leer' | 'codewort_falsch'"""
    text = (user.get("text_head") or "")
    own = user.get("code") or ""
    if any(c in text for c in codes if c != own):
        return "uebersprechen"
    if int(user.get("predicted_n") or 0) < 32:
        return "leer"
    if own not in text:
        return "codewort_falsch"
    return "ok"


def rows(since: str = "") -> list[dict]:
    if not RESULTS.is_file():
        return []
    out = []
    for line in RESULTS.read_text().splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("kind") != "parallel" or not d.get("users"):
            continue
        if since and str(d.get("when", "")) < since:
            continue
        out.append(d)
    return out


def summarize(d: dict) -> dict:
    per = d.get("details", {}).get("per_user", [])
    agg = d.get("details", {}).get("aggregate", {})
    codes = [u.get("code") for u in per if u.get("code")]
    kinds = [classify(u, codes) for u in per if "error" not in u]
    return {
        "quant": d.get("quant"), "users": d.get("users"), "when": d.get("when"),
        "ctx_per_slot": d.get("details", {}).get("ctx_per_slot"),
        "prompt_tokens": agg.get("prompt_tokens"), "gen_tokens": agg.get("gen_tokens"),
        "agg_tps": d.get("agg_tps"), "user_tps": d.get("tg_tps"), "user_min": agg.get("user_tg_min"),
        "ttft_p50": d.get("ttft_p50"), "ttft_p95": d.get("ttft_p95"),
        "draft_accept": agg.get("draft_accept"), "draft_n": agg.get("draft_n"),
        "ok": kinds.count("ok"), "uebersprechen": kinds.count("uebersprechen"),
        "leer": kinds.count("leer"), "codewort_falsch": kinds.count("codewort_falsch"),
        "n": len(kinds),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="", help="nur Läufe ab diesem Zeitstempel (z.B. 2026-09-05T21:00)")
    ap.add_argument("--markdown", action="store_true")
    a = ap.parse_args()

    data = [r for r in (summarize(d) for d in rows(a.since)) if r["n"]]   # abgebrochene Stufen weglassen
    if not data:
        print("keine passenden Läufe in", RESULTS)
        return 1

    if a.markdown:
        print("| Quant | Nutzer | Σ t/s | je Nutzer | min | TTFT p50 | Akzeptanz | ok | leer | Codewort falsch | Übersprechen |")
        print("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for r in data:
            print(f"| {r['quant']} | {r['users']} | {r['agg_tps']:.1f} | {r['user_tps']:.1f} | {r['user_min']:.1f} | "
                  f"{r['ttft_p50']:.0f} s | {r['draft_accept']:.2f} | {r['ok']}/{r['n']} | {r['leer']} | "
                  f"{r['codewort_falsch']} | {r['uebersprechen']} |")
        return 0

    print(f"{'Quant':12} {'N':>2} {'Σ t/s':>7} {'je Nutzer':>9} {'min':>5} {'TTFT':>6} {'Akzept':>7} "
          f"{'ok':>5} {'leer':>4} {'CW!':>4} {'Übspr':>5}")
    for r in data:
        print(f"{r['quant']:12} {r['users']:>2} {r['agg_tps']:7.1f} {r['user_tps']:9.1f} {r['user_min']:5.1f} "
              f"{r['ttft_p50']:5.0f}s {r['draft_accept']:7.2f} {r['ok']:>2}/{r['n']:<2} {r['leer']:>4} "
              f"{r['codewort_falsch']:>4} {r['uebersprechen']:>5}")
    print("\nok = eigenes Codewort korrekt wiedergegeben · leer = unter 32 Token · CW! = Codewort fehlt oder verfälscht"
          "\nÜbspr = echtes Übersprechen (fremdes Codewort in der Antwort)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
