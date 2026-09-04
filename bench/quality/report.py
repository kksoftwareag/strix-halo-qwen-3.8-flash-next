#!/usr/bin/env python3
"""Ergebnisse der Terminal-Bench-Mini-Läufe einsammeln und aufbereiten.

Liest die exportierten Ergebnisse aus state/quality/tbench, die Aufgaben-Metadaten aus dem
Benchmark und die genauen Server-Kommandos aus den Lauf-Logs. Schreibt:

  docs/tbmini-data.js    Datensatz für die interaktive Seite (window.TBMINI = {...})
  docs/TERMINAL-BENCH.md Dokumentation mit Tabellen

  bench/quality/report.py [--results DIR] [--out-json DATEI] [--out-md DATEI]
"""
from __future__ import annotations

import argparse
import json
import re
import tomllib
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
TASKS_DIR = HERE / "terminal-bench-mini" / "tasks"
SUBSET = HERE / "terminal-bench-mini" / "subsets" / "full.txt"
RESULTS = PROJECT / "state" / "quality" / "tbench"
LOGS = PROJECT / "state" / "quality"

# Reihenfolge der Quants von klein nach groß
QUANT_ORDER = ["UD-Q2_K_XL", "UD-IQ3_XXS", "UD-IQ4_XS", "UD-Q4_K_XL"]
# Messwerte aus docs/RESEARCH.md (unsloth-KLD-Tabelle)
QUANT_FACTS = {
    "UD-Q2_K_XL": {"file_gib": 73.4, "kld": 0.2246, "top1": 82.7, "footprint_gib": 59.2},
    "UD-IQ3_XXS": {"file_gib": 76.3, "kld": 0.1651, "top1": 85.4, "footprint_gib": 62.0},
    "UD-IQ4_XS": {"file_gib": 87.2, "kld": 0.0836, "top1": 89.6, "footprint_gib": 72.9},
    "UD-Q4_K_XL": {"file_gib": 103.7, "kld": 0.0469, "top1": 92.3, "footprint_gib": 92.3},
}


def task_meta() -> list[dict]:
    order = [ln.strip() for ln in SUBSET.read_text().splitlines() if ln.strip()] if SUBSET.is_file() else []
    out = []
    for name in order or sorted(p.name for p in TASKS_DIR.iterdir() if (p / "task.toml").is_file()):
        f = TASKS_DIR / name / "task.toml"
        if not f.is_file():
            continue
        t = tomllib.loads(f.read_text())
        m, env, ag = t.get("metadata", {}), t.get("environment", {}), t.get("agent", {})
        out.append({
            "id": name,
            "description": (t.get("task", {}) or {}).get("description", ""),
            "difficulty": m.get("difficulty", ""),
            "category": m.get("category", ""),
            "expert_min": m.get("expert_time_estimate_min"),
            "task_timeout_s": ag.get("timeout_sec"),
            "memory_mb": env.get("memory_mb"),
            "image": env.get("docker_image", ""),
        })
    return out


def server_commands() -> dict[str, dict]:
    """Zu jedem Quant das exakte Server-Kommando und die Speicherbilanz aus dem Lauf-Log."""
    out: dict[str, dict] = {}
    for log in sorted(LOGS.glob("tbmini-*.log")):
        quant = log.name[len("tbmini-"):-len(".log")]
        text = log.read_text(errors="replace")
        entry: dict = {"log": str(log.relative_to(PROJECT))}
        m = re.search(r"^   Server-Log    (\S+)$", text, re.M)
        if m:
            p = Path(m.group(1))
            entry["server_log"] = str(p.relative_to(PROJECT)) if p.is_absolute() and PROJECT in p.parents else str(p)
            if p.is_file():
                first = p.open(errors="replace").readline().strip()
                if first.startswith("# "):
                    entry["command"] = first[2:]
        mem = re.findall(r"^   ([A-ZÄÖÜa-zä-ü][^\n]*?)\s{2,}([\d.,]+ GiB)$", text, re.M)
        if mem:
            entry["memory"] = [[k.strip(), v] for k, v in mem]
        m = re.search(r"^   Kontext       (\d+) gesamt, (\d+) je Slot \((\d+) Slots\)$", text, re.M)
        if m:
            entry["ctx_total"], entry["ctx_per_slot"], entry["slots"] = int(m[1]), int(m[2]), int(m[3])
        m = re.search(r"^   apt-Spiegel\s+(.*)$", text, re.M)
        if m:
            entry["apt_mirror"] = m.group(1).strip()
        out[quant] = entry
    return out


def load_runs(results: Path) -> list[dict]:
    runs = []
    for summary in sorted(results.glob("*/*_results/summary.json")):
        s = json.loads(summary.read_text())
        per = {}
        for rf in sorted(summary.parent.glob("results-*.json")):
            r = json.loads(rf.read_text())
            att = (r.get("attempts") or [{}])[0]
            per[r["task"]] = {
                "passed": bool(r.get("passed")),
                "reward": r.get("reward"),
                "duration_s": round((r.get("duration_ms") or 0) / 1000),
                "steps": r.get("agent_steps"),
                "tokens": r.get("tokens") or {},
                "peak_context": (att.get("tokens") or {}).get("peak_context"),
                "exception": att.get("exception"),
                "attempts": len(r.get("attempts") or []),
            }
        prof = s.get("evaluation_profile") or {}
        runs.append({
            "quant": s.get("quant"),
            "inference_profile": s.get("inference_profile"),
            "engine": s.get("engine"),
            "engine_version": s.get("engine_version"),
            "backend": s.get("backend"),
            "backend_version": s.get("backend_version"),
            "platform": (s.get("platform") or {}).get("name"),
            "model": (s.get("model") or {}).get("name"),
            "n_ctx": ((((s.get("model") or {}).get("endpoint_metadata") or {}).get("meta")) or {}).get("n_ctx"),
            "benchmark": prof.get("benchmark"),
            "tb_version": prof.get("terminal_bench_version"),
            "tb_revision": prof.get("terminal_bench_revision"),
            "harbor_version": prof.get("harbor_version"),
            "generated_at": s.get("generated_at"),
            "total_tasks": s.get("total_tasks"),
            "passed_tasks": s.get("passed_tasks"),
            "pass_rate": s.get("pass_rate"),
            "duration_s": round((s.get("total_duration_ms") or 0) / 1000),
            "tokens": s.get("tokens") or {},
            "dir": str(summary.parent.relative_to(PROJECT)),
            "per_task": per,
        })
    runs.sort(key=lambda r: (QUANT_ORDER.index(r["quant"]) if r["quant"] in QUANT_ORDER else 99, r["quant"] or ""))
    return runs


def hms(seconds: float) -> str:
    seconds = int(seconds or 0)
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def markdown(data: dict) -> str:
    tasks, runs = data["tasks"], data["runs"]
    full = [r for r in runs if (r["total_tasks"] or 0) >= 20]
    part = [r for r in runs if (r["total_tasks"] or 0) < 20]
    L: list[str] = []
    add = L.append
    add("# Terminal-Bench-Mini-20: Ergebnisse\n")
    add(f"Stand: {data['generated_at'][:10]}. Agenten-Benchmark mit 20 Aufgaben aus Terminal-Bench "
        f"{full[0]['tb_version'] if full else '2.1'} auf dieser Maschine, ein Quant nach dem anderen. "
        "Aufbau und Bedienung: [`bench/quality/README.md`](../bench/quality/README.md), Einordnung in "
        "[`QUALITAETS-BENCHMARKS.md`](QUALITAETS-BENCHMARKS.md).\n")

    add("## Ergebnis\n")
    if full:
        add("| Quant | bestanden | Quote | Dauer | Ausgabe-Token | Token/s im Mittel | KLD | Top-1 |")
        add("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for r in full:
            f = QUANT_FACTS.get(r["quant"], {})
            out_tok = (r["tokens"] or {}).get("output") or 0
            tps = out_tok / r["duration_s"] if r["duration_s"] else 0
            add(f"| {r['quant']} | {r['passed_tasks']}/{r['total_tasks']} | {r['pass_rate']:.0%} | "
                f"{hms(r['duration_s'])} h | {out_tok:,} | {tps:.1f} | {f.get('kld', '')} | {f.get('top1', '')} % |"
                .replace(",", "."))
    else:
        add("_Noch keine vollständigen Läufe._")
    add("")

    if full:
        add("## Aufgaben im Einzelnen\n")
        head = "| Aufgabe | Kategorie | Schwierigkeit | " + " | ".join(r["quant"] for r in full) + " |"
        add(head)
        add("| --- | --- | --- | " + " | ".join("---" for _ in full) + " |")
        for t in tasks:
            cells = []
            for r in full:
                d = r["per_task"].get(t["id"])
                if not d:
                    cells.append("–")
                elif d["passed"]:
                    cells.append(f"**ja** ({hms(d['duration_s'])})")
                elif d.get("exception"):
                    cells.append("Fehler")
                else:
                    cells.append(f"nein ({hms(d['duration_s'])})")
            add(f"| `{t['id']}` | {t['category']} | {t['difficulty']} | " + " | ".join(cells) + " |")
        add("")

    add("## Ausführung\n")
    add(f"- Benchmark: {full[0]['benchmark'] if full else 'Terminal-Bench-Local'}, Terminal-Bench "
        f"{full[0]['tb_version'] if full else '2.1'} (Revision `{full[0]['tb_revision'][:12] if full else ''}`), "
        f"Harbor {full[0]['harbor_version'] if full else '0.20.0'}, Agent Terminus-2")
    add("- Ein Versuch je Aufgabe (pass@1), ein Stream (`-np 1`), MTP als Draft-Head aktiv")
    add("- Zeitlimit 1800 s je Aufgabe statt der 3 Stunden des Benchmarks; das liegt bei 18 der 20 Aufgaben "
        "über dem Limit, das die Aufgabe selbst vorgibt (Ausnahmen: `build-pov-ray` mit 12000 s und "
        "`fix-ocaml-gc` mit 3600 s)")
    add("- Container je Aufgabe: 1 CPU, 2 GB RAM (nur `overfull-hbox`: 2 CPUs, 4 GB)")
    if full:
        r = full[0]
        add(f"- Engine: {r['engine']} {r['engine_version']}, Backend {r['backend']} {r['backend_version']}, "
            f"Kontext {r['n_ctx']}")
    add("")
    cmds = data.get("commands") or {}
    for r in full + part:
        c = cmds.get(r["quant"]) or {}
        if not c.get("command"):
            continue
        add(f"### {r['quant']}\n")
        add("```bash")
        add(c["command"])
        add("```")
        if c.get("memory"):
            add("")
            add("| Posten | Größe |")
            add("| --- | --- |")
            for k, v in c["memory"]:
                add(f"| {k} | {v} |")
        add("")
    if part:
        add("## Weitere Läufe\n")
        for r in part:
            add(f"- {r['quant']}: {r['passed_tasks']}/{r['total_tasks']} Aufgaben "
                f"({hms(r['duration_s'])}), Profil `{r['inference_profile']}`")
        add("")
    add("Rohdaten: `state/quality/tbench/`, Transkripte und Verifier-Ausgaben unter "
        "`bench/quality/terminal-bench-mini/jobs/`. Interaktive Ansicht: "
        "[terminal-bench.html](terminal-bench.html).")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default=str(RESULTS))
    ap.add_argument("--out-json", default=str(PROJECT / "docs" / "tbmini-data.js"))
    ap.add_argument("--out-md", default=str(PROJECT / "docs" / "TERMINAL-BENCH.md"))
    a = ap.parse_args()

    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tasks": task_meta(),
        "runs": load_runs(Path(a.results)),
        "commands": server_commands(),
        "quant_facts": QUANT_FACTS,
    }
    Path(a.out_json).write_text("window.TBMINI = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")
    Path(a.out_md).write_text(markdown(data))
    print(f"{len(data['runs'])} Läufe, {len(data['tasks'])} Aufgaben -> {a.out_json}, {a.out_md}")
    for r in data["runs"]:
        print(f"  {r['quant']:12} {r['passed_tasks']}/{r['total_tasks']}  {hms(r['duration_s'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
