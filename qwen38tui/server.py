"""Prozess-Manager für `llama serve` + HTTP-Client für Health/Slots/Metrics/Testanfragen."""
from __future__ import annotations

import asyncio
import json
import os
import re
import signal
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Awaitable, Callable

import httpx

from .config import Command
from .discovery import STATE_DIR
from .memory import record_measurement

LOG_DIR = STATE_DIR / "logs"

LineCallback = Callable[[str], None]


@dataclass
class ServerStats:
    """Aus Log-Zeilen / Antworten extrahierte Kennzahlen."""
    model_buffer_mib: float = 0.0
    kv_buffer_mib: float = 0.0
    compute_buffer_mib: float = 0.0
    draft_model_mib: float = 0.0
    lazy_tensors: list[str] = field(default_factory=list)
    attn_rot_k: int | None = None
    attn_rot_v: int | None = None
    n_ctx: int = 0
    load_seconds: float = 0.0
    last_pp_tps: float = 0.0
    last_tg_tps: float = 0.0
    last_prompt_n: int = 0
    last_gen_n: int = 0
    draft_n: int = 0
    draft_accepted: int = 0
    requests: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def accept_rate(self) -> float:
        return self.draft_accepted / self.draft_n if self.draft_n else 0.0


_RE_MIB = re.compile(r"(model|KV|compute|CPU_Mapped model|ROCm0 model|Vulkan0 model)[^=\n]*buffer size\s*=\s*([\d.]+)\s*MiB", re.I)


class ServerProcess:
    """Startet/stoppt den Server, liest stdout/stderr asynchron und schreibt ein Logfile."""

    def __init__(self) -> None:
        self.proc: asyncio.subprocess.Process | None = None
        self.command: Command | None = None
        self.started_at: float = 0.0
        self.log_path: Path | None = None
        self.stats = ServerStats()
        self._reader_task: asyncio.Task | None = None
        self._log_fh = None
        self.exit_code: int | None = None
        self.ready: bool = False

    # ------------------------------------------------------------------
    @property
    def running(self) -> bool:
        return self.proc is not None and self.proc.returncode is None

    @property
    def pid(self) -> int | None:
        return self.proc.pid if self.proc else None

    @property
    def uptime(self) -> float:
        return time.time() - self.started_at if self.running else 0.0

    # ------------------------------------------------------------------
    async def start(self, cmd: Command, on_line: LineCallback) -> None:
        if self.running:
            raise RuntimeError("Server läuft bereits")
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        self.log_path = LOG_DIR / f"server-{datetime.now():%Y%m%d-%H%M%S}.log"
        self._log_fh = self.log_path.open("w", buffering=1)
        self._log_fh.write("# " + cmd.shell() + "\n")
        env = dict(os.environ)
        env.update(cmd.env)
        self.command = cmd
        self.stats = ServerStats()
        self.ready = False
        self.exit_code = None
        self.started_at = time.time()
        self.proc = await asyncio.create_subprocess_exec(
            *cmd.argv, env=env, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
            start_new_session=True,
        )
        self._reader_task = asyncio.create_task(self._read(on_line))

    async def _read(self, on_line: LineCallback) -> None:
        assert self.proc and self.proc.stdout
        try:
            while True:
                raw = await self.proc.stdout.readline()
                if not raw:
                    break
                line = raw.decode("utf-8", errors="replace").rstrip("\n")
                self._parse(line)
                if self._log_fh:
                    self._log_fh.write(line + "\n")
                on_line(line)
        except asyncio.CancelledError:
            # App wird beendet: nicht auf den (minutenlangen) Server-Teardown warten
            self._close_log("# reader cancelled")
            raise
        self.exit_code = await self.proc.wait()
        self._close_log(f"# exit {self.exit_code}")
        on_line(f"[server beendet, exit {self.exit_code}]")

    def _close_log(self, tail: str) -> None:
        if self._log_fh:
            try:
                self._log_fh.write(tail + "\n")
                self._log_fh.close()
            except Exception:
                pass
            self._log_fh = None

    def _parse(self, line: str) -> None:
        s = self.stats
        m = _RE_MIB.search(line)
        if m:
            kind, val = m.group(1).lower(), float(m.group(2))
            if "kv" in kind:
                s.kv_buffer_mib += val
            elif "compute" in kind:
                s.compute_buffer_mib = max(s.compute_buffer_mib, val)
            else:
                s.model_buffer_mib += val
        m = re.search(r"tensor (\S+) \(size = (\d+) MiB\) lazy read enabled", line)
        if m:
            s.lazy_tensors.append(f"{m.group(1)} ({int(m.group(2)) / 1024:.1f} GiB)")
        m = re.search(r"attn_rot_k = (\d)", line)
        if m:
            s.attn_rot_k = int(m.group(1))
        m = re.search(r"attn_rot_v = (\d)", line)
        if m:
            s.attn_rot_v = int(m.group(1))
        m = re.search(r"n_ctx_slot = (\d+)", line)
        if m:
            s.n_ctx = int(m.group(1))
        if "model loaded" in line and not s.load_seconds:
            s.load_seconds = time.time() - self.started_at
        if re.search(r"listening on|server is listening", line):
            self.ready = True
        m = re.search(r"prompt eval time\s*=\s*([\d.]+) ms /\s*(\d+) tokens.*?([\d.]+) tokens per second", line)
        if m:
            s.last_prompt_n, s.last_pp_tps = int(m.group(2)), float(m.group(3))
        m = re.search(r"\beval time\s*=\s*([\d.]+) ms /\s*(\d+) tokens.*?([\d.]+) tokens per second", line)
        if m and "prompt" not in line:
            s.last_gen_n, s.last_tg_tps = int(m.group(2)), float(m.group(3))
            s.requests += 1
        m = re.search(r"draft acceptance(?: rate)?\s*=\s*([\d.]+)\s*\(\s*(\d+) accepted /\s*(\d+) generated", line)
        if m:
            s.draft_accepted += int(m.group(2))
            s.draft_n += int(m.group(3))
        if re.search(r"\bE \w|error|failed to|cannot|Error", line) and "0 errors" not in line:
            s.errors.append(line[-200:])
        elif re.search(r"\bW \w|warn", line, re.I):
            s.warnings.append(line[-200:])

    def record_measurements(self, quant: str, ubatch: int, flash_attn: str) -> None:
        s = self.stats
        if s.compute_buffer_mib:
            record_measurement(f"compute:{quant}:{ubatch}:{flash_attn}",
                               {"compute": int(s.compute_buffer_mib * 2**20), "model_mib": s.model_buffer_mib,
                                "kv_mib": s.kv_buffer_mib, "ts": time.time()})

    async def stop(self, grace: float = 180.0) -> int | None:
        """SIGINT (sauberer Shutdown; dauert bei 50–80 GiB GTT bis zu Minuten), danach SIGKILL.
        Ein zweites SIGINT/SIGTERM würde den Server sofort mit exit(1) beenden, deshalb nur ein Signal + Kill."""
        if not self.proc or self.proc.returncode is not None:
            return self.exit_code
        try:
            os.killpg(self.proc.pid, signal.SIGINT)
        except ProcessLookupError:
            pass
        try:
            await asyncio.wait_for(self.proc.wait(), grace)
        except asyncio.TimeoutError:
            try:
                os.killpg(self.proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            await self.proc.wait()
        if self._reader_task:
            try:
                await asyncio.wait_for(self._reader_task, 5)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                pass
        self.exit_code = self.proc.returncode
        return self.exit_code


# ----------------------------------------------------------------------------------------------
class ServerClient:
    """Dünner HTTP-Client für llama-server."""

    def __init__(self, host: str, port: int, api_key: str = "") -> None:
        h = "127.0.0.1" if host in ("0.0.0.0", "::", "") else host
        self.base = f"http://{h}:{port}"
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    async def _get(self, path: str, timeout: float = 5.0) -> Any:
        async with httpx.AsyncClient(timeout=timeout, headers=self.headers) as c:
            r = await c.get(self.base + path)
            r.raise_for_status()
            ct = r.headers.get("content-type", "")
            return r.json() if "json" in ct else r.text

    async def health(self) -> dict[str, Any]:
        try:
            d = await self._get("/health")
            return d if isinstance(d, dict) else {"status": str(d)}
        except httpx.HTTPStatusError as e:
            try:
                return e.response.json()
            except Exception:
                return {"status": f"http {e.response.status_code}"}
        except Exception as e:
            return {"status": "offline", "error": e.__class__.__name__}

    async def props(self) -> dict[str, Any]:
        try:
            d = await self._get("/props")
            return d if isinstance(d, dict) else {}
        except Exception:
            return {}

    async def slots(self) -> list[dict[str, Any]]:
        try:
            d = await self._get("/slots")
            return d if isinstance(d, list) else []
        except Exception:
            return []

    async def metrics(self) -> dict[str, float]:
        """Prometheus-Text -> {name: value} (nur llamacpp:*-Zähler)."""
        try:
            txt = await self._get("/metrics")
        except Exception:
            return {}
        out: dict[str, float] = {}
        for line in str(txt).splitlines():
            if line.startswith("llamacpp:"):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        out[parts[0]] = float(parts[1])
                    except ValueError:
                        pass
        return out

    async def wait_ready(self, timeout: float = 600.0, poll: float = 2.0, should_abort: Callable[[], bool] | None = None) -> bool:
        t0 = time.time()
        while time.time() - t0 < timeout:
            if should_abort and should_abort():
                return False
            h = await self.health()
            if h.get("status") == "ok":
                return True
            await asyncio.sleep(poll)
        return False

    async def chat(self, prompt: str, *, max_tokens: int = 256, temperature: float | None = None, timeout: float = 600.0,
                   system: str | None = None, on_token: Callable[[str], Awaitable[None] | None] | None = None) -> dict[str, Any]:
        """Eine Chat-Completion (streaming) – liefert Text + timings des Servers."""
        msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
        body: dict[str, Any] = {"messages": msgs, "max_tokens": max_tokens, "stream": True, "timings_per_token": False}
        if temperature is not None:
            body["temperature"] = temperature
        text, reasoning, timings = [], [], {}
        t0 = time.time()
        t_first: float | None = None
        async with httpx.AsyncClient(timeout=timeout, headers=self.headers) as c:
            async with c.stream("POST", self.base + "/v1/chat/completions", json=body) as r:
                r.raise_for_status()
                async for line in r.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    payload = line[5:].strip()
                    if payload == "[DONE]":
                        break
                    try:
                        obj = json.loads(payload)
                    except json.JSONDecodeError:
                        continue
                    if "timings" in obj:
                        timings = obj["timings"]
                    for ch in obj.get("choices", []):
                        delta = ch.get("delta", {})
                        if t_first is None and (delta.get("content") or delta.get("reasoning_content")):
                            t_first = time.time() - t0
                        if delta.get("content"):
                            text.append(delta["content"])
                            if on_token:
                                res = on_token(delta["content"])
                                if asyncio.iscoroutine(res):
                                    await res
                        if delta.get("reasoning_content"):
                            reasoning.append(delta["reasoning_content"])
        return {"text": "".join(text), "reasoning": "".join(reasoning), "timings": timings, "wall": time.time() - t0,
                "ttft": t_first if t_first is not None else time.time() - t0}


def port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host if host not in ("0.0.0.0", "auto", "") else "127.0.0.1", port)) == 0
