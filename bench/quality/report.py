#!/usr/bin/env python3
"""Collect and prepare the results of the Terminal-Bench-Mini runs.

Reads the exported results from state/quality/tbench, the task metadata from the benchmark
and the exact server command lines from the run logs. Writes:

  docs/tbmini-data.js    data set for the interactive page (window.TBMINI = {...})
  docs/TERMINAL-BENCH.md documentation with tables

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
RESULTS2 = PROJECT / "state" / "quality" / "tbench-versuch2"   # zweiter Versuch
RESULTS3 = PROJECT / "state" / "quality" / "tbench-versuch3"   # third attempt, time-limit cases only
LOGS = PROJECT / "state" / "quality"

# quant order, smallest first
QUANT_ORDER = ["UD-IQ1_M", "UD-Q2_K_XL", "UD-IQ3_XXS", "UD-IQ4_XS", "UD-Q4_K_XL"]
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
    """For each quant: the exact server command line and the memory breakdown from the run log."""
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
    """Extra details from the Harbor trial: episodes and the duration of the longest model request."""
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
    """Sum up throughput and MTP acceptance from the server log."""
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
        prof0 = s.get("inference_profile") or ""
        effort = ("aus" if "no-thinking" in prof0 else
                  next((e for e in ("xhigh", "medium", "low") if f"thinking-{e}" in prof0), "?"))
        for rf in sorted(summary.parent.glob("results-*.json")):
            r = json.loads(rf.read_text())
            att = (r.get("attempts") or [{}])[0]
            det = trial_details(((att.get("harbor_paths") or {}).get("trial")))
            tfile = summary.parent / f"transcript-{r['task']}.json"
            exc_type = det.get("exception_type") or (att.get("exception") or None)
            per[r["task"]] = {
                "passed": bool(r.get("passed")),
                "reward": r.get("reward"),
                "duration_s": round((r.get("duration_ms") or 0) / 1000),
                "steps": r.get("agent_steps"),
                "tokens": r.get("tokens") or {},
                "peak_context": (att.get("tokens") or {}).get("peak_context"),
                "exception": att.get("exception"),
                "outcome": ("passed" if r.get("passed") else
                            "time limit" if exc_type == "AgentTimeoutError" else
                            "aborted" if exc_type else "not passed"),
                "exception_type": det.get("exception_type"),
                "exception_message": det.get("exception_message"),
                "episodes": det.get("episodes"),
                "requests": det.get("requests"),
                "model_s": det.get("model_s"),
                "tok_per_s": det.get("tok_per_s"),
                "req_max_s": det.get("req_max_s"),
                "req_mean_s": det.get("req_mean_s"),
                "attempts": len(r.get("attempts") or []),
                "transcript": (f"transcripts/{run_slug(s.get('quant'), effort)}/{r['task']}.json"
                               if tfile.is_file() else None),
            }
        prof = s.get("evaluation_profile") or {}
        if not prof:
            first = next(iter(sorted(summary.parent.glob("results-*.json"))), None)
            if first:
                prof = json.loads(first.read_text()).get("evaluation_profile") or {}
        profile = prof0
        runs.append({
            "quant": s.get("quant"),
            "inference_profile": profile,
            "effort": effort,
            "label": f"{s.get('quant')} · {effort}" + (f" · {s.get('tag')}" if s.get("tag") else ""),
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
    zweite, dritte = second_attempts(RESULTS2), second_attempts(RESULTS3)
    for r in runs:
        per2 = zweite.get((r["quant"], r["effort"])) or {}
        per3 = dritte.get((r["quant"], r["effort"])) or {}
        for task, d2 in per2.items():
            if task in r["per_task"]:
                r["per_task"][task]["attempt2"] = d2
        for task, d3 in per3.items():
            if task in r["per_task"]:
                r["per_task"][task]["attempt3"] = d3
        r["passed_2"] = sum(1 for t, d in r["per_task"].items()
                            if d["passed"] or (d.get("attempt2") or {}).get("passed"))
        r["passed_3"] = sum(1 for t, d in r["per_task"].items()
                            if d["passed"] or (d.get("attempt2") or {}).get("passed")
                            or (d.get("attempt3") or {}).get("passed"))
        durs = sorted(d["duration_s"] for d in r["per_task"].values() if d.get("duration_s"))
        r["task_mean_s"] = round(sum(durs) / len(durs)) if durs else None
        r["task_median_s"] = durs[len(durs) // 2] if durs else None
        r["task_max_s"] = durs[-1] if durs else None
        r["has_attempt2"] = bool(per2)
        r["has_attempt3"] = bool(per3)
        r["attempt2_timeout_s"] = next((d.get("timeout_s") for d in per2.values() if d.get("timeout_s")), None)
        r["attempt3_timeout_s"] = next((d.get("timeout_s") for d in per3.values() if d.get("timeout_s")), None)

    effort_order = {"aus": 0, "low": 1, "medium": 2, "xhigh": 3}
    runs.sort(key=lambda r: (effort_order.get(r["effort"], 9),
                             QUANT_ORDER.index(r["quant"]) if r["quant"] in QUANT_ORDER else 99, r["quant"] or ""))
    return runs


REPO_RESULTS = HERE / "results"
DOCS_TRANSCRIPTS = PROJECT / "docs" / "transcripts"


# Die Speicherbilanz kommt aus dem deutschsprachigen Programm; für die englische Doku übersetzt.
MEMORY_LABELS = {
    "Gewichte (resident)": "weights (resident)",
    "PLE-Tabelle lazy (nicht resident)": "embedding table, lazy (not resident)",
    "KV-Cache (12 Attn-Layer)": "KV cache (12 attention layers)",
    "Indexer-Cache": "indexer cache",
    "DeltaNet-Zustand": "DeltaNet state",
    "Compute-Buffer (gemessen)": "compute buffer (measured)",
    "Compute-Buffer (Schätzung)": "compute buffer (estimated)",
    "MTP-Head + Draft-KV": "MTP head + draft KV",
    "Prompt-Cache (max)": "prompt cache (max)",
    "Summe": "total",
    "Verfügbar (MemAvailable)": "available (MemAvailable)",
    "Reserve OS/Page-Cache": "reserved for OS/page cache",
    "Spielraum": "headroom",
}


def run_slug(quant: str | None, effort: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", f"{quant or 'unbekannt'}-{effort}")


def copy_results(results: Path) -> tuple[int, int]:
    """Mirror results into the repo: metrics to bench/quality/results, transcripts to docs/."""
    n = t = 0
    for summary in sorted(results.glob("*/*_results/summary.json")):
        src = summary.parent
        dst = REPO_RESULTS / src.parent.name / src.name
        dst.mkdir(parents=True, exist_ok=True)
        meta = json.loads(summary.read_text())
        prof = meta.get("inference_profile") or ""
        effort = ("aus" if "no-thinking" in prof else
                  next((e for e in ("xhigh", "medium", "low") if f"thinking-{e}" in prof), "?"))
        tdst = DOCS_TRANSCRIPTS / run_slug(meta.get("quant"), effort)
        for f in sorted(src.iterdir()):
            if not f.is_file():
                continue
            if f.name.startswith("transcript-"):
                tdst.mkdir(parents=True, exist_ok=True)
                target = tdst / f.name[len("transcript-"):]
                if not target.exists() or target.stat().st_size != f.stat().st_size:
                    target.write_bytes(f.read_bytes())
                t += 1
            else:
                (dst / f.name).write_bytes(f.read_bytes())
                n += 1
    return n, t



def second_attempts(root: Path) -> dict[tuple[str, str], dict]:
    """Results of the second attempt, keyed by (quant, reasoning effort)."""
    out: dict[tuple[str, str], dict] = {}
    if not root.is_dir():
        return out
    for summary in sorted(root.glob("*/*_results/summary.json")):
        s = json.loads(summary.read_text())
        prof = s.get("inference_profile") or ""
        effort = ("aus" if "no-thinking" in prof else
                  next((e for e in ("xhigh", "medium", "low") if f"thinking-{e}" in prof), "?"))
        per = {}
        for rf in sorted(summary.parent.glob("results-*.json")):
            r = json.loads(rf.read_text())
            att = (r.get("attempts") or [{}])[0]
            det = trial_details((att.get("harbor_paths") or {}).get("trial"))
            exc = det.get("exception_type")
            per[r["task"]] = {
                "passed": bool(r.get("passed")),
                "duration_s": round((r.get("duration_ms") or 0) / 1000),
                "outcome": ("passed" if r.get("passed") else
                            "time limit" if exc == "AgentTimeoutError" else
                            "aborted" if exc else "not passed"),
                "tokens": r.get("tokens") or {},
                "steps": r.get("agent_steps"),
                "episodes": det.get("episodes"),
                "model_s": det.get("model_s"),
                "tok_per_s": det.get("tok_per_s"),
                "timeout_s": ((json.loads(rf.read_text()).get("evaluation_profile") or {}).get("agent_timeout_seconds")),
            }
        out[(s.get("quant"), effort)] = per
    return out

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
    add("# Terminal-Bench-Mini-20: results\n")
    add(f"As of {data['generated_at'][:10]}. Agent benchmark with 20 tasks from Terminal-Bench "
        f"{(full[0].get('tb_version') if full else None) or '2.1'} on this machine, one quant after another. "
        "Setup and usage: [`bench/quality/README.md`](../bench/quality/README.md), context in "
        "[`QUALITY-BENCHMARKS.md`](QUALITY-BENCHMARKS.md).\n")

    add("## Result\n")
    if full:
        zwei = any(r.get("has_attempt2") for r in full)
        drei = any(r.get("has_attempt3") for r in full)
        add("| Quant | pass@1 | " + ("pass@2 | " if zwei else "") + ("pass@3 | " if drei else "") +
            "Duration | avg per task | median | output tokens | tokens/s over the run | KLD | top-1 |")
        add("| --- | --- | " + ("--- | " if zwei else "") + ("--- | " if drei else "") +
            "--- | --- | --- | --- | --- | --- | --- |")
        for r in full:
            f = QUANT_FACTS.get(r["quant"], {})
            out_tok = (r["tokens"] or {}).get("output") or 0
            tps = out_tok / r["duration_s"] if r["duration_s"] else 0
            p2 = ""
            if zwei:
                n2 = r.get("passed_2", r["passed_tasks"])
                p2 = (f"**{n2}/{r['total_tasks']}** | " if n2 > r["passed_tasks"] else f"{n2}/{r['total_tasks']} | ")
            if drei:
                n3 = r.get("passed_3", r.get("passed_2", r["passed_tasks"]))
                p2 += (f"**{n3}/{r['total_tasks']}** | " if n3 > r.get("passed_2", 0) else f"{n3}/{r['total_tasks']} | ")
            add(f"| {r['label']} | {r['passed_tasks']}/{r['total_tasks']} | {p2}"
                f"{hm(r['duration_s'])} | {hms(r['task_mean_s'] or 0)} | {hms(r['task_median_s'] or 0)} | "
                f"{out_tok:,} | {tps:.1f} | {f.get('kld', '–')} | "
                f"{str(f.get('top1', '–')) + ('%' if f.get('top1') else '')} |")
        if zwei:
            tmo = next((r.get("attempt2_timeout_s") for r in full if r.get("attempt2_timeout_s")), None)
            add("")
            gescheitert = sum(1 for r in full for d in r["per_task"].values() if not d["passed"])
            wiederholt = sum(1 for r in full for d in r["per_task"].values() if d.get("attempt2"))
            t1 = full[0].get("agent_timeout_s") or 3600
            if wiederholt >= gescheitert:
                add(f"pass@2: every task that failed in the first round got exactly one second attempt, with a "
                    f"{tmo or 5400} s time limit instead of {t1} s.")
            else:
                add(f"pass@2: a second attempt with {tmo or 5400} s instead of {t1} s has run for {wiederholt} of the "
                    f"{gescheitert} failed tasks so far; for the rest, pass@2 = pass@1.")
            if drei:
                t3 = next((r.get("attempt3_timeout_s") for r in full if r.get("attempt3_timeout_s")), 10800)
                add(f"pass@3 counts a third attempt with {t3} s, run only for the tasks that hit the time limit in the "
                    "second attempt as well.")
            add("")
            add("\u201cAvg per task\u201d and \u201cmedian\u201d refer to the first round and count the full time per "
                "task: container setup, the agent's work and the verifier.")
    else:
        add("_No complete runs yet._")
    add("")

    if full:
        add("## Tasks in detail\n")
        head = "| Task | Category | Difficulty | " + " | ".join(r["label"] for r in full) + " |"
        add(head)
        add("| --- | --- | --- | " + " | ".join("---" for _ in full) + " |")
        for t in tasks:
            cells = []
            for r in full:
                d = r["per_task"].get(t["id"])
                if not d:
                    cells.append("–")
                elif d["passed"]:
                    cells.append(f"**yes** ({hms(d['duration_s'])})")
                else:
                    txt = f"{d.get('outcome', 'no')} ({hms(d['duration_s'])})"
                    for a in (d.get("attempt2"), d.get("attempt3")):
                        if a:
                            txt += (f" → **yes** ({hms(a['duration_s'])})" if a["passed"]
                                    else f" → {a.get('outcome', 'no')} ({hms(a['duration_s'])})")
                    cells.append(txt)
            add(f"| `{t['id']}` | {t['category']} | {t['difficulty']} | " + " | ".join(cells) + " |")
        add("")

    if full:
        add("## How to read this\n")
        add("The project the benchmark comes from publishes runs of other models on comparable hardware "
            "(Strix Halo, 128 GB): 11 to 18 of 20 tasks — but with **two** attempts per task and a three-hour time "
            "limit. The numbers here are measured with one attempt and are therefore on the conservative side.\n")
        add("Two caveats before comparing quants on individual tasks:\n")
        add("- With 20 tasks, the 95% interval around a result is about ±11 percentage points. A difference of one "
            "or two tasks between two quants is noise.")
        add("- Measurements use `temp 1.0`, so they are not deterministic. In a discarded preliminary run with a "
            "30-minute limit, `configure-git-webserver` passed; in the run that counts, it did not — with an agent "
            "that finished after seven minutes, that was not the time limit.")
        add("")

        add("## Throughput and draft acceptance\n")
        add("| Quant | requests | prompt tokens | generated tokens | prompt t/s | decode t/s | MTP acceptance | mean draft length |")
        add("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for r in full:
            cmds0 = data.get("commands") or {}
            st = ((cmds0.get(r["log_key"]) or cmds0.get(r["quant"]) or {}).get("server")) or {}
            def g(key):
                v = st.get(key)
                return f"{v:,}" if isinstance(v, int) else ("–" if v is None else str(v))
            add(f"| {r['label']} | {g('requests')} | {g('prompt_tokens')} | {g('generated_tokens')} | "
                f"{g('pp_tps')} | {g('tg_tps')} | {g('draft_accept')} | {g('draft_mean_len')} |")
        add("")
        add("The values come from the server log of each run (all requests the agent made, not only the answers "
            "that count towards the score). `Decode t/s` is the pure generation rate, averaged over all requests.")
        add("")

        add("### Speed per task\n")
        add("Output tokens divided by the time the agent actually waited for the model (the sum of all response "
            "times). The value is below the pure decode rate because every request also processes the prompt; it "
            "says how fast the agent made progress on that task.\n")
        add("| Task | " + " | ".join(f"{r['label']} t/s" for r in full) + " | " +
            " | ".join(f"{r['label']} model time" for r in full) + " |")
        add("| --- | " + " | ".join("---" for _ in full * 2) + " |")
        for t in tasks:
            rates, times = [], []
            for r in full:
                d = r["per_task"].get(t["id"]) or {}
                rates.append(f"{d['tok_per_s']:.1f}" if d.get("tok_per_s") else "–")
                times.append(hms(d["model_s"]) if d.get("model_s") else "–")
            add(f"| `{t['id']}` | " + " | ".join(rates) + " | " + " | ".join(times) + " |")
        add("")
        for r in full:
            vals = [d["tok_per_s"] for d in r["per_task"].values() if d.get("tok_per_s")]
            secs = sum(d["model_s"] for d in r["per_task"].values() if d.get("model_s"))
            toks = sum((d.get("tokens") or {}).get("output") or 0 for d in r["per_task"].values())
            if vals:
                add(f"- {r['label']}: {min(vals):.1f} to {max(vals):.1f} t/s per task, {toks / secs:.1f} t/s "
                    f"across all tasks; the agent waited {hm(secs)} for the model, which is "
                    f"{secs / r['duration_s'] * 100:.0f}% of the run time.")
        add("")

    add("## How it was run\n")
    ref = full[0] if full else {}
    rev = (ref.get("tb_revision") or "")[:12]
    add(f"- Benchmark: {ref.get('benchmark') or 'Terminal-Bench-Local'}, Terminal-Bench "
        f"{ref.get('tb_version') or '2.1'}{f' (revision `{rev}`)' if rev else ''}, "
        f"Harbor {ref.get('harbor_version') or '0.20.0'}, Agent Terminus-2")
    add("- One attempt per task (pass@1), a single stream (`-np 1`), MTP draft head active, "
        "`reasoning_effort: medium`")
    tmo = next((r.get("agent_timeout_s") for r in full if r.get("agent_timeout_s")), None)
    if tmo:
        above = sum(1 for t in tasks if (t.get("task_timeout_s") or 0) <= tmo)
        add(f"- Time limit {tmo} s per task instead of the 3 hours the benchmark defaults to; for "
            f"{above} of the {len(tasks)} tasks that is above the limit the task itself specifies")
    add("- Container per task: 1 CPU, 2 GB RAM (only `overfull-hbox`: 2 CPUs, 4 GB)")
    if full:
        r = full[0]
        add(f"- Engine: {r['engine']} {r['engine_version']}, backend {r['backend']} {r['backend_version']}, "
            f"context {r['n_ctx']}")
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
            add("| Item | Size |")
            add("| --- | --- |")
            for k, v in c["memory"]:
                add(f"| {MEMORY_LABELS.get(k, k)} | {v} |")
        add("")
    if part:
        add("## Other runs\n")
        for r in part:
            add(f"- {r['label']}: {r['passed_tasks']}/{r['total_tasks']} tasks "
                f"({hm(r['duration_s'])}), profile `{r['inference_profile']}`")
        add("")
    add("Raw data: `state/quality/tbench/`, transcripts and verifier output under "
        "`bench/quality/terminal-bench-mini/jobs/`. Interactive view: "
        "[terminal-bench.html](terminal-bench.html).")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default=str(RESULTS))
    ap.add_argument("--out-json", default=str(PROJECT / "docs" / "tbmini-data.js"))
    ap.add_argument("--out-md", default=str(PROJECT / "docs" / "TERMINAL-BENCH.md"))
    ap.add_argument("--no-copy", action="store_true", help="do not mirror results into the repo")
    a = ap.parse_args()

    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tasks": task_meta(),
        "runs": load_runs(Path(a.results)),
        "commands": server_commands(),
        "quant_facts": QUANT_FACTS,
    }
    if not a.no_copy:
        n, t = copy_results(Path(a.results))
        print(f"mirrored {n} result files to {REPO_RESULTS.relative_to(PROJECT)} and "
              f"{t} transcripts to {DOCS_TRANSCRIPTS.relative_to(PROJECT)}")
    Path(a.out_json).write_text("window.TBMINI = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")
    Path(a.out_md).write_text(markdown(data))
    print(f"{len(data['runs'])} runs, {len(data['tasks'])} tasks -> {a.out_json}, {a.out_md}")
    for r in data["runs"]:
        print(f"  {r['quant']:12} {r['passed_tasks']}/{r['total_tasks']}  {hms(r['duration_s'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
