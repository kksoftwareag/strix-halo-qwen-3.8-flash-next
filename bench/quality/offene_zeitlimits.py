#!/usr/bin/env python3
"""Gibt 'QUANT:aufgabe1,aufgabe2' für jede Aufgabe aus, deren jüngster Versuch am Zeitlimit
gescheitert ist – und die im nächsten Versuchsordner noch fehlt.

  bench/quality/offene_zeitlimits.py [--von tbench-versuch2] [--nach tbench-versuch3]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
TBM = PROJECT / "bench" / "quality" / "terminal-bench-mini"
ORDER = ["UD-IQ1_M", "UD-Q2_K_XL", "UD-IQ3_XXS", "UD-IQ4_XS", "UD-Q4_K_XL"]


def timeout_tasks(root: Path) -> dict[str, set[str]]:
    """Aufgaben, die in diesem Ergebnisordner am Zeitlimit gescheitert sind."""
    out: dict[str, set[str]] = {}
    for summary in sorted(root.glob("*/*_results/summary.json")):
        quant = json.loads(summary.read_text()).get("quant")
        for f in sorted(summary.parent.glob("results-*.json")):
            r = json.loads(f.read_text())
            if r.get("passed"):
                continue
            att = (r.get("attempts") or [{}])[0]
            trial = (att.get("harbor_paths") or {}).get("trial")
            typ = ""
            if trial and (TBM / trial / "result.json").is_file():
                typ = (json.loads((TBM / trial / "result.json").read_text()).get("exception_info")
                       or {}).get("exception_type") or ""
            if typ == "AgentTimeoutError":
                out.setdefault(quant, set()).add(r["task"])
    return out


def done(root: Path) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for summary in sorted(root.glob("*/*_results/summary.json")):
        quant = json.loads(summary.read_text()).get("quant")
        out.setdefault(quant, set()).update(
            json.loads(f.read_text())["task"] for f in summary.parent.glob("results-*.json"))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--von", default="state/quality/tbench-versuch2")
    ap.add_argument("--nach", default="state/quality/tbench-versuch3")
    a = ap.parse_args()
    offen = timeout_tasks(PROJECT / a.von)
    fertig = done(PROJECT / a.nach)
    for quant in ORDER:
        rest = sorted(offen.get(quant, set()) - fertig.get(quant, set()))
        if rest:
            print(f"{quant}:{','.join(rest)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
