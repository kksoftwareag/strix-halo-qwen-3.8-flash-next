#!/usr/bin/env python3
"""Gibt 'QUANT:aufgabe1,aufgabe2' für jede im ersten Durchgang gescheiterte Aufgabe aus,
die im zweiten Ergebnisordner noch fehlt. Reihenfolge: kleinster Quant zuerst."""
from __future__ import annotations

import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
R1 = PROJECT / "state" / "quality" / "tbench"
R2 = PROJECT / "state" / "quality" / "tbench-versuch2"
ORDER = ["UD-IQ1_M", "UD-Q2_K_XL", "UD-IQ3_XXS", "UD-IQ4_XS", "UD-Q4_K_XL"]


def failed(root: Path) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for summary in sorted(root.glob("*/*_results/summary.json")):
        s = json.loads(summary.read_text())
        if (s.get("total_tasks") or 0) < 20:
            continue
        tasks = {json.loads(f.read_text())["task"] for f in summary.parent.glob("results-*.json")
                 if not json.loads(f.read_text()).get("passed")}
        out.setdefault(s.get("quant"), set()).update(tasks)
    return out


def done(root: Path) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for summary in sorted(root.glob("*/*_results/summary.json")):
        s = json.loads(summary.read_text())
        out.setdefault(s.get("quant"), set()).update(
            json.loads(f.read_text())["task"] for f in summary.parent.glob("results-*.json"))
    return out


def main() -> int:
    offen, fertig = failed(R1), done(R2)
    for quant in ORDER:
        rest = sorted(offen.get(quant, set()) - fertig.get(quant, set()))
        if rest:
            print(f"{quant}:{','.join(rest)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
