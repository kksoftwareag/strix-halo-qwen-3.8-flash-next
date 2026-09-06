#!/usr/bin/env python3
"""Gibt 'QUANT:aufgabe1,aufgabe2' für jede im ersten Durchgang gescheiterte Aufgabe aus,
die im zweiten Ergebnisordner noch fehlt. Reihenfolge: kleinster Quant zuerst.

  offene_wiederholungen.py [--effort medium]   # nur Läufe dieser Denkstufe
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
R1 = PROJECT / "state" / "quality" / "tbench"
R2 = PROJECT / "state" / "quality" / "tbench-versuch2"
ORDER = ["UD-IQ1_M", "UD-Q2_K_XL", "UD-IQ3_XXS", "UD-IQ4_XS", "UD-Q4_K_XL"]


def effort_of(summary: dict) -> str:
    prof = summary.get("inference_profile") or ""
    if "no-thinking" in prof:
        return "aus"
    return next((e for e in ("xhigh", "medium", "low") if f"thinking-{e}" in prof), "?")


def failed(root: Path, effort: str) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for summary in sorted(root.glob("*/*_results/summary.json")):
        s = json.loads(summary.read_text())
        if (s.get("total_tasks") or 0) < 20 or effort_of(s) != effort:
            continue
        tasks = {json.loads(f.read_text())["task"] for f in summary.parent.glob("results-*.json")
                 if not json.loads(f.read_text()).get("passed")}
        out.setdefault(s.get("quant"), set()).update(tasks)
    return out


def done(root: Path, effort: str) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for summary in sorted(root.glob("*/*_results/summary.json")):
        s = json.loads(summary.read_text())
        if effort_of(s) != effort:
            continue
        out.setdefault(s.get("quant"), set()).update(
            json.loads(f.read_text())["task"] for f in summary.parent.glob("results-*.json"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--effort", default="medium")
    a = ap.parse_args()
    offen, fertig = failed(R1, a.effort), done(R2, a.effort)
    for quant in ORDER:
        rest = sorted(offen.get(quant, set()) - fertig.get(quant, set()))
        if rest:
            print(f"{quant}:{','.join(rest)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
