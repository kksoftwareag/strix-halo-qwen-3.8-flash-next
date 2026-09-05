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
    "UD-IQ1_M": {"file_gib": 69.4, "kld": 0.3147, "top1": 79.7, "footprint_gib": 55.1},
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
        key = log.name[len("tbmini-"):-len(".log")]
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
                entry["server"] = server_stats(p)
        mem = re.findall(r"^   ([A-ZÄÖÜa-zä-ü][^\n]*?)\s{2,}([\d.,]+ GiB)$", text, re.M)
        if mem:
            entry["memory"] = [[k.strip(), v] for k, v in mem]
        m = re.search(r"^   Kontext       (\d+) gesamt, (\d+) je Slot \((\d+) Slots\)$", text, re.M)
        if m:
            entry["ctx_total"], entry["ctx_per_slot"], entry["slots"] = int(m[1]), int(m[2]), int(m[3])
        m = re.search(r"^   apt-Spiegel\s+(.*)$", text, re.M)
        if m:
            entry["apt_mirror"] = m.group(1).strip()
        out[key] = entry
    return out


JOBS = HERE / "terminal-bench-mini"


def trial_details(rel_trial: str | None) -> dict:
    """Zusatzangaben aus dem Harbor-Trial: Episoden und Dauer der längsten Modellanfrage."""
    if not rel_trial:
        return {}
    f = JOBS / rel_trial / "result.json"
    if not f.is_file():
        return {}
    try:
        d = json.loads(f.read_text())
    except (OSError, json.JSONDecodeError):
        return {}
    meta = ((d.get("agent_result") or {}).get("metadata") or {})
    times = meta.get("api_request_times_msec") or []
    exc = d.get("exception_info") or {}
    out = {"episodes": meta.get("n_episodes")}
    if times:
        model_s = sum(times) / 1000
        out["requests"] = len(times)
        out["req_max_s"] = round(max(times) / 1000)
        out["req_mean_s"] = round(sum(times) / len(times) / 1000)
        out["model_s"] = round(model_s)
        n_out = (d.get("agent_result") or {}).get("n_output_tokens") or 0
        if model_s > 0 and n_out:
            out["tok_per_s"] = round(n_out / model_s, 1)
    if exc:
        out["exception_type"] = exc.get("exception_type")
        out["exception_message"] = exc.get("exception_message")
    return out


RE_PROMPT = re.compile(r"prompt eval time =\s*([\d.]+) ms /\s*(\d+) tokens")
RE_EVAL = re.compile(r"\|\s+eval time =\s*([\d.]+) ms /\s*(\d+) tokens")
RE_DRAFT = re.compile(r"draft acceptance = ([\d.]+) \(\s*(\d+) accepted /\s*(\d+) generated\), mean len =\s*([\d.]+)")


def server_stats(path: Path) -> dict:
    """Durchsatz und MTP-Akzeptanz aus dem Server-Log zusammenzählen."""
    if not path.is_file():
        return {}
    text = path.read_text(errors="replace")
    pp_ms = pp_tok = tg_ms = tg_tok = 0.0
    for ms, tok in RE_PROMPT.findall(text):
        pp_ms += float(ms); pp_tok += int(tok)
    for ms, tok in RE_EVAL.findall(text):
        tg_ms += float(ms); tg_tok += int(tok)
    acc = gen = 0
    lens = []
    for _, a, g, ln in RE_DRAFT.findall(text):
        acc += int(a); gen += int(g); lens.append(float(ln))
    out = {
        "requests": len(RE_EVAL.findall(text)),
        "prompt_tokens": int(pp_tok),
        "generated_tokens": int(tg_tok),
        "pp_tps": round(pp_tok / (pp_ms / 1000), 1) if pp_ms else None,
        "tg_tps": round(tg_tok / (tg_ms / 1000), 1) if tg_ms else None,
    }
    if gen:
        out["draft_accept"] = round(acc / gen, 3)
        out["draft_mean_len"] = round(sum(lens) / len(lens), 2)
    m2 = re.search(r"^(\d+)\.(\d+)\.(\d+)\.(\d+) I srv .*model loaded", text, re.M)
    if m2:
        out["load_s"] = int(m2[1]) * 60 + int(m2[2])
    return out


def load_runs(results: Path) -> list[dict]:
    runs = []
    for summary in sorted(results.glob("*/*_results/summary.json")):
        s = json.loads(summary.read_text())
        per = {}
        for rf in sorted(summary.parent.glob("results-*.json")):
            r = json.loads(rf.read_text())
            att = (r.get("attempts") or [{}])[0]
            det = trial_details(((att.get("harbor_paths") or {}).get("trial")))
            exc_type = det.get("exception_type") or (att.get("exception") or None)
            per[r["task"]] = {
                "passed": bool(r.get("passed")),
                "reward": r.get("reward"),
                "duration_s": round((r.get("duration_ms") or 0) / 1000),
                "steps": r.get("agent_steps"),
                "tokens": r.get("tokens") or {},
                "peak_context": (att.get("tokens") or {}).get("peak_context"),
                "exception": att.get("exception"),
                "outcome": ("bestanden" if r.get("passed") else
                            "Zeitlimit" if exc_type == "AgentTimeoutError" else
                            "Abbruch" if exc_type else "nicht bestanden"),
                "exception_type": det.get("exception_type"),
                "exception_message": det.get("exception_message"),
                "episodes": det.get("episodes"),
                "requests": det.get("requests"),
                "model_s": det.get("model_s"),
                "tok_per_s": det.get("tok_per_s"),
                "req_max_s": det.get("req_max_s"),
                "req_mean_s": det.get("req_mean_s"),
                "attempts": len(r.get("attempts") or []),
            }
        prof = s.get("evaluation_profile") or {}
        if not prof:
            first = next(iter(sorted(summary.parent.glob("results-*.json"))), None)
            if first:
                prof = json.loads(first.read_text()).get("evaluation_profile") or {}
        profile = s.get("inference_profile") or ""
        effort = ("aus" if "no-thinking" in profile else
                  next((e for e in ("xhigh", "medium", "low") if f"thinking-{e}" in profile), "?"))
        runs.append({
            "quant": s.get("quant"),
            "inference_profile": profile,
            "effort": effort,
            "label": f"{s.get('quant')} · {effort}",
            "log_key": f"{s.get('quant')}-{effort}" if effort != "medium" else str(s.get("quant")),
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
            "agent_timeout_s": prof.get("agent_timeout_seconds"),
            "generated_at": s.get("generated_at"),
            "total_tasks": s.get("total_tasks"),
            "passed_tasks": s.get("passed_tasks"),
            "pass_rate": s.get("pass_rate"),
            "duration_s": round((s.get("total_duration_ms") or 0) / 1000),
            "tokens": s.get("tokens") or {},
            "dir": str(summary.parent.relative_to(PROJECT)),
            "per_task": per,
        })
    effort_order = {"aus": 0, "low": 1, "medium": 2, "xhigh": 3}
    runs.sort(key=lambda r: (effort_order.get(r["effort"], 9),
                             QUANT_ORDER.index(r["quant"]) if r["quant"] in QUANT_ORDER else 99, r["quant"] or ""))
    return runs


REPO_RESULTS = HERE / "results"


def copy_results(results: Path) -> int:
    """Ergebnisse (ohne die großen Transkripte) ins Repo spiegeln, damit sie versioniert sind."""
    n = 0
    for summary in sorted(results.glob("*/*_results/summary.json")):
        src = summary.parent
        dst = REPO_RESULTS / src.parent.name / src.name
        dst.mkdir(parents=True, exist_ok=True)
        for f in sorted(src.iterdir()):
            if f.is_file() and not f.name.startswith("transcript-"):
                (dst / f.name).write_bytes(f.read_bytes())
                n += 1
    return n


def hm(seconds: float) -> str:
    seconds = int(seconds or 0)
    h, m = divmod(seconds // 60, 60)
    return f"{h} h {m} min" if h else f"{m} min"


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
        f"{(full[0].get('tb_version') if full else None) or '2.1'} auf dieser Maschine, ein Quant nach dem anderen. "
        "Aufbau und Bedienung: [`bench/quality/README.md`](../bench/quality/README.md), Einordnung in "
        "[`QUALITAETS-BENCHMARKS.md`](QUALITAETS-BENCHMARKS.md).\n")

    add("## Ergebnis\n")
    if full:
        add("| Quant | bestanden | Quote | Dauer | Ausgabe-Token | Token/s über die Laufzeit | KLD | Top-1 |")
        add("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for r in full:
            f = QUANT_FACTS.get(r["quant"], {})
            out_tok = (r["tokens"] or {}).get("output") or 0
            tps = out_tok / r["duration_s"] if r["duration_s"] else 0
            add(f"| {r['label']} | {r['passed_tasks']}/{r['total_tasks']} | {r['pass_rate']:.0%} | "
                f"{hm(r['duration_s'])} | {out_tok:,} | {tps:.1f} | {f.get('kld', '–')} | "
                f"{str(f.get('top1', '–')) + (' %' if f.get('top1') else '')} |".replace(",", "."))
    else:
        add("_Noch keine vollständigen Läufe._")
    add("")

    if full:
        add("## Aufgaben im Einzelnen\n")
        head = "| Aufgabe | Kategorie | Schwierigkeit | " + " | ".join(r["label"] for r in full) + " |"
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
                else:
                    cells.append(f"{d.get('outcome', 'nein')} ({hms(d['duration_s'])})")
            add(f"| `{t['id']}` | {t['category']} | {t['difficulty']} | " + " | ".join(cells) + " |")
        add("")

    if full:
        add("## Einordnung\n")
        add("Das Projekt, aus dem der Benchmark stammt, veröffentlicht Läufe anderer Modelle auf vergleichbarer "
            "Hardware (Strix Halo, 128 GB): 11 bis 18 von 20 Aufgaben – allerdings mit **zwei** Versuchen je Aufgabe "
            "und einem Zeitlimit von drei Stunden. Die Zahlen hier sind mit einem Versuch gemessen und deshalb eher "
            "konservativ.\n")
        add("Zwei Dinge dazu, bevor man Quants anhand einzelner Aufgaben vergleicht:\n")
        add("- Bei 20 Aufgaben liegt das 95-%-Intervall um ein Ergebnis bei rund ±11 Prozentpunkten. Ein Unterschied "
            "von ein bis zwei Aufgaben zwischen zwei Quants ist Rauschen.")
        add("- Gemessen wird mit `temp 1.0`, also nicht deterministisch. In einem verworfenen Vorlauf mit 30-Minuten-"
            "Limit war `configure-git-webserver` bestanden, im gewerteten Lauf nicht – bei einem Agenten, der nach "
            "sieben Minuten fertig war, lag das nicht am Zeitlimit.")
        add("")

        add("## Durchsatz und Draft-Akzeptanz\n")
        add("| Quant | Anfragen | Prompt-Token | erzeugte Token | Prompt t/s | Decode t/s | MTP-Akzeptanz | mittlere Draft-Länge |")
        add("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for r in full:
            cmds0 = data.get("commands") or {}
            st = ((cmds0.get(r["log_key"]) or cmds0.get(r["quant"]) or {}).get("server")) or {}
            def g(key):
                v = st.get(key)
                return f"{v:,}".replace(",", ".") if isinstance(v, int) else ("–" if v is None else str(v))
            add(f"| {r['label']} | {g('requests')} | {g('prompt_tokens')} | {g('generated_tokens')} | "
                f"{g('pp_tps')} | {g('tg_tps')} | {g('draft_accept')} | {g('draft_mean_len')} |")
        add("")
        add("Die Werte stammen aus dem Server-Log des jeweiligen Laufs (alle Anfragen des Agenten, "
            "nicht nur die Antworten, die in die Wertung eingehen). `Decode t/s` ist die reine "
            "Erzeugungsrate, gemittelt über alle Anfragen.")
        add("")

        add("### Tempo je Aufgabe\n")
        add("Ausgabe-Token geteilt durch die Zeit, die der Agent tatsächlich auf das Modell gewartet hat "
            "(Summe aller Antwortzeiten). Der Wert liegt unter der reinen Decode-Rate, weil jede Anfrage "
            "auch den Prompt verarbeitet; er sagt, wie schnell der Agent bei dieser Aufgabe vorankam.\n")
        add("| Aufgabe | " + " | ".join(f"{r['label']} t/s" for r in full) + " | " +
            " | ".join(f"{r['label']} Modellzeit" for r in full) + " |")
        add("| --- | " + " | ".join("---" for _ in full * 2) + " |")
        for t in tasks:
            rates, times = [], []
            for r in full:
                d = r["per_task"].get(t["id"]) or {}
                rates.append(f"{d['tok_per_s']:.1f}".replace(".", ",") if d.get("tok_per_s") else "–")
                times.append(hms(d["model_s"]) if d.get("model_s") else "–")
            add(f"| `{t['id']}` | " + " | ".join(rates) + " | " + " | ".join(times) + " |")
        add("")
        for r in full:
            vals = [d["tok_per_s"] for d in r["per_task"].values() if d.get("tok_per_s")]
            secs = sum(d["model_s"] for d in r["per_task"].values() if d.get("model_s"))
            toks = sum((d.get("tokens") or {}).get("output") or 0 for d in r["per_task"].values())
            if vals:
                komma = lambda x, n=1: f"{x:.{n}f}".replace(".", ",")
                add(f"- {r['label']}: {komma(min(vals))} bis {komma(max(vals))} t/s je Aufgabe, über alle "
                    f"Aufgaben {komma(toks / secs)} t/s; der Agent wartete {hm(secs)} auf das Modell, "
                    f"das sind {secs / r['duration_s'] * 100:.0f} % der Laufzeit.")
        add("")

    add("## Ausführung\n")
    ref = full[0] if full else {}
    rev = (ref.get("tb_revision") or "")[:12]
    add(f"- Benchmark: {ref.get('benchmark') or 'Terminal-Bench-Local'}, Terminal-Bench "
        f"{ref.get('tb_version') or '2.1'}{f' (Revision `{rev}`)' if rev else ''}, "
        f"Harbor {ref.get('harbor_version') or '0.20.0'}, Agent Terminus-2")
    add("- Ein Versuch je Aufgabe (pass@1), ein Stream (`-np 1`), MTP als Draft-Head aktiv, "
        "`reasoning_effort: medium`")
    tmo = next((r.get("agent_timeout_s") for r in full if r.get("agent_timeout_s")), None)
    if tmo:
        über = sum(1 for t in tasks if (t.get("task_timeout_s") or 0) <= tmo)
        add(f"- Zeitlimit {tmo} s je Aufgabe statt der 3 Stunden, die der Benchmark voreinstellt; bei "
            f"{über} der {len(tasks)} Aufgaben liegt das über dem Limit, das die Aufgabe selbst vorgibt")
    add("- Container je Aufgabe: 1 CPU, 2 GB RAM (nur `overfull-hbox`: 2 CPUs, 4 GB)")
    if full:
        r = full[0]
        add(f"- Engine: {r['engine']} {r['engine_version']}, Backend {r['backend']} {r['backend_version']}, "
            f"Kontext {r['n_ctx']}")
    add("")
    cmds = data.get("commands") or {}
    for r in full + part:
        c = cmds.get(r["log_key"]) or cmds.get(r["quant"]) or {}
        if not c.get("command"):
            continue
        add(f"### {r['label']}\n")
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
            add(f"- {r['label']}: {r['passed_tasks']}/{r['total_tasks']} Aufgaben "
                f"({hm(r['duration_s'])}), Profil `{r['inference_profile']}`")
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
    ap.add_argument("--no-copy", action="store_true", help="Ergebnisse nicht ins Repo spiegeln")
    a = ap.parse_args()

    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tasks": task_meta(),
        "runs": load_runs(Path(a.results)),
        "commands": server_commands(),
        "quant_facts": QUANT_FACTS,
    }
    if not a.no_copy:
        n = copy_results(Path(a.results))
        print(f"{n} Ergebnisdateien nach {REPO_RESULTS.relative_to(PROJECT)} gespiegelt")
    Path(a.out_json).write_text("window.TBMINI = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")
    Path(a.out_md).write_text(markdown(data))
    print(f"{len(data['runs'])} Läufe, {len(data['tasks'])} Aufgaben -> {a.out_json}, {a.out_md}")
    for r in data["runs"]:
        print(f"  {r['quant']:12} {r['passed_tasks']}/{r['total_tasks']}  {hms(r['duration_s'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
