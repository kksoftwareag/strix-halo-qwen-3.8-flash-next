window.TBMINI = {
 "generated_at": "2026-09-04T21:01:45+00:00",
 "tasks": [
  {
   "id": "pypi-server",
   "description": "Evaluates the ability to create a Python package, build it, set up a local PyPI server, and make the package installable from the server.",
   "difficulty": "medium",
   "category": "software-engineering",
   "expert_min": 60.0,
   "task_timeout_s": 900.0,
   "memory_mb": 2048,
   "image": "alexgshaw/pypi-server:20251031"
  },
  {
   "id": "nginx-request-logging",
   "description": "Evaluates the ability to install and configure Nginx with advanced request logging, rate limiting, and custom error pages.",
   "difficulty": "medium",
   "category": "system-administration",
   "expert_min": 20.0,
   "task_timeout_s": 900.0,
   "memory_mb": 2048,
   "image": "alexgshaw/nginx-request-logging:20251031"
  },
  {
   "id": "git-leak-recovery",
   "description": "Evaluates the ability to recover secrets from unreachable git objects and completely remove them from repository history while preserving legitimate commits.",
   "difficulty": "medium",
   "category": "software-engineering",
   "expert_min": 30.0,
   "task_timeout_s": 900.0,
   "memory_mb": 2048,
   "image": "alexgshaw/git-leak-recovery:20251031"
  },
  {
   "id": "fix-git",
   "description": "Evaluates the ability to recover lost Git commits from a detached HEAD state and merge them back into the master branch.",
   "difficulty": "easy",
   "category": "software-engineering",
   "expert_min": 5.0,
   "task_timeout_s": 900.0,
   "memory_mb": 2048,
   "image": "alexgshaw/fix-git:20260403"
  },
  {
   "id": "cobol-modernization",
   "description": "Evaluates the ability to reverse-engineer and reimplement a COBOL program's business logic in Python with exact output reproduction.",
   "difficulty": "easy",
   "category": "software-engineering",
   "expert_min": 20.0,
   "task_timeout_s": 900.0,
   "memory_mb": 2048,
   "image": "alexgshaw/cobol-modernization:20251031"
  },
  {
   "id": "regex-log",
   "description": "Tests the ability to construct a complex regular expression that matches dates in log lines containing valid IPv4 addresses while handling edge cases and boundary conditions.",
   "difficulty": "medium",
   "category": "data-processing",
   "expert_min": 45.0,
   "task_timeout_s": 900.0,
   "memory_mb": 2048,
   "image": "alexgshaw/regex-log:20251031"
  },
  {
   "id": "headless-terminal",
   "description": "Implement a Python class that provides a headless terminal interface supporting interactive bash shells, modifier keys, startup file sourcing, and state persistence between commands.",
   "difficulty": "medium",
   "category": "software-engineering",
   "expert_min": 120.0,
   "task_timeout_s": 900.0,
   "memory_mb": 2048,
   "image": "alexgshaw/headless-terminal:20251031"
  },
  {
   "id": "mailman",
   "description": "Evaluates the ability to configure a functional mailing list server by integrating postfix and mailman3 with proper join/leave/announce workflows.",
   "difficulty": "medium",
   "category": "system-administration",
   "expert_min": 60.0,
   "task_timeout_s": 1800.0,
   "memory_mb": 2048,
   "image": "alexgshaw/mailman:20251031"
  },
  {
   "id": "fix-ocaml-gc",
   "description": "Evaluates ability to debug and fix a runtime crash in the OCaml garbage collector's C implementation, requiring low-level debugging skills and understanding of compiler internals.",
   "difficulty": "hard",
   "category": "software-engineering",
   "expert_min": 1440.0,
   "task_timeout_s": 3600.0,
   "memory_mb": 2048,
   "image": "alexgshaw/fix-ocaml-gc:20251031"
  },
  {
   "id": "break-filter-js-from-html",
   "description": "Evaluates the agent's ability to bypass an HTML sanitization filter by crafting malicious HTML that triggers JavaScript execution after filtering.",
   "difficulty": "medium",
   "category": "security",
   "expert_min": 20.0,
   "task_timeout_s": 1200.0,
   "memory_mb": 2048,
   "image": "alexgshaw/break-filter-js-from-html:20251031"
  },
  {
   "id": "sqlite-with-gcov",
   "description": "Evaluates the ability to compile SQLite from source with gcov instrumentation and make it available in the system PATH.",
   "difficulty": "medium",
   "category": "system-administration",
   "expert_min": 30.0,
   "task_timeout_s": 900.0,
   "memory_mb": 2048,
   "image": "alexgshaw/sqlite-with-gcov:20251031"
  },
  {
   "id": "sparql-university",
   "description": "Evaluates the ability to write complex SPARQL queries with multiple constraints, aggregations, and date filtering against an RDF knowledge graph.",
   "difficulty": "hard",
   "category": "data-querying",
   "expert_min": 800.0,
   "task_timeout_s": 900.0,
   "memory_mb": 2048,
   "image": "alexgshaw/sparql-university:20251031"
  },
  {
   "id": "llm-inference-batching-scheduler",
   "description": "Implement a shape-aware batching scheduler for static-graph LLM inference that optimally packs requests into batches while meeting strict performance thresholds on cost, latency, and padding.",
   "difficulty": "hard",
   "category": "machine-learning",
   "expert_min": 45.0,
   "task_timeout_s": 1800.0,
   "memory_mb": 2048,
   "image": "alexgshaw/llm-inference-batching-scheduler:20251031"
  },
  {
   "id": "configure-git-webserver",
   "description": "Evaluates the ability to configure a Git server with automatic deployment to an nginx web server using post-receive hooks.",
   "difficulty": "hard",
   "category": "system-administration",
   "expert_min": 15.0,
   "task_timeout_s": 900.0,
   "memory_mb": 2048,
   "image": "alexgshaw/configure-git-webserver:20251031"
  },
  {
   "id": "build-cython-ext",
   "description": "Evaluates the ability to compile and install a Python package with Cython extensions from source while fixing NumPy 2.x compatibility issues.",
   "difficulty": "medium",
   "category": "debugging",
   "expert_min": 60.0,
   "task_timeout_s": 900.0,
   "memory_mb": 2048,
   "image": "alexgshaw/build-cython-ext:20251031"
  },
  {
   "id": "extract-elf",
   "description": "Evaluates ability to parse ELF binary format and extract memory values from executable sections using Node.js.",
   "difficulty": "medium",
   "category": "file-operations",
   "expert_min": 30.0,
   "task_timeout_s": 900.0,
   "memory_mb": 2048,
   "image": "alexgshaw/extract-elf:20251031"
  },
  {
   "id": "build-pov-ray",
   "description": "Evaluates the ability to locate, download, patch, and compile legacy POV-Ray 2.2 raytracer from 1990s source archives on a modern system.",
   "difficulty": "medium",
   "category": "software-engineering",
   "expert_min": 60.0,
   "task_timeout_s": 12000.0,
   "memory_mb": 2048,
   "image": "alexgshaw/build-pov-ray:20251031"
  },
  {
   "id": "openssl-selfsigned-cert",
   "description": "Evaluates an agent's ability to generate self-signed TLS certificates using OpenSSL, manage cryptographic keys with proper permissions, and create verification scripts.",
   "difficulty": "medium",
   "category": "security",
   "expert_min": 20.0,
   "task_timeout_s": 900.0,
   "memory_mb": 2048,
   "image": "alexgshaw/openssl-selfsigned-cert:20251031"
  },
  {
   "id": "overfull-hbox",
   "description": "Evaluates the ability to fix LaTeX overfull hbox warnings by replacing words with valid synonyms while satisfying compilation and constraint requirements.",
   "difficulty": "easy",
   "category": "debugging",
   "expert_min": 60.0,
   "task_timeout_s": 750.0,
   "memory_mb": 4096,
   "image": "alexgshaw/overfull-hbox:20260403"
  },
  {
   "id": "mteb-retrieve",
   "description": "Evaluates the agent's ability to perform semantic text retrieval using MTEB embeddings, computing cosine similarities and correctly ranking documents to find the 5th most similar match to a query.",
   "difficulty": "medium",
   "category": "data-science",
   "expert_min": 15.0,
   "task_timeout_s": 1800.0,
   "memory_mb": 2048,
   "image": "alexgshaw/mteb-retrieve:20260430"
  }
 ],
 "runs": [
  {
   "quant": "UD-Q2_K_XL",
   "inference_profile": "mtp4-ngram-thinking-medium",
   "engine": "llama.cpp",
   "engine_version": "0.3.0-dev (build 1, commit 60bce1a)",
   "backend": "rocm",
   "backend_version": "7.1.52802",
   "platform": "AMD Ryzen AI MAX+ 395 (Strix Halo)",
   "model": "Qwen3.8-Flash-Next",
   "n_ctx": 163840,
   "benchmark": "Terminal-Bench-Local",
   "tb_version": "2.1",
   "tb_revision": "5c8eadf1f393183288fa08b8f73ca9a469cc5e00",
   "harbor_version": "0.20.0",
   "agent_timeout_s": 3600,
   "generated_at": "2026-09-04T20:57:22.815082+00:00",
   "total_tasks": 20,
   "passed_tasks": 16,
   "pass_rate": 0.8,
   "duration_s": 27360,
   "tokens": {
    "input": 7666917,
    "cached": 7262286,
    "output": 385970
   },
   "dir": "state/quality/tbench/strix-halo/qwen3.8-flash-da666201-llama.cpp-rocm-UD-Q2_K_XL-mtp4-ngram-thinking-me_results",
   "per_task": {
    "break-filter-js-from-html": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 3460,
     "steps": 12,
     "tokens": {
      "input": 73145,
      "cached": 66794,
      "output": 21736
     },
     "peak_context": 9339,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 12,
     "requests": 12,
     "req_max_s": 1839,
     "req_mean_s": 277,
     "attempts": 1
    },
    "build-cython-ext": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1807,
     "steps": 65,
     "tokens": {
      "input": 1268478,
      "cached": 1236262,
      "output": 18912
     },
     "peak_context": 31960,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 65,
     "requests": 65,
     "req_max_s": 61,
     "req_mean_s": 14,
     "attempts": 1
    },
    "build-pov-ray": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 3644,
     "steps": 64,
     "tokens": {
      "input": 2629929,
      "cached": 2558332,
      "output": 34498
     },
     "peak_context": 71345,
     "exception": {
      "exception_type": "AgentTimeoutError",
      "exception_message": "Agent execution timed out after 3600.0 seconds",
      "exception_traceback": "Traceback (most recent call last):\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 488, in wait_for\n    return await fut\n           ^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1607, in run\n    await self._run_agent_loop(\n    ...<3 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1286, in _run_agent_loop\n    ) = await self._handle_llm_interaction(\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, self._session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1164, in _handle_llm_interaction\n    llm_response = await self._query_llm(\n                   ^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1004, in _query_llm\n    llm_response = await chat.chat(\n                   ^^^^^^^^^^^^^^^^\n    ...<2 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/llms/chat.py\", line 89, in chat\n    llm_response: LLMResponse = await self._model.call(\n                                ^^^^^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/llms/lite_llm.py\", line 370, in call\n    response = await litellm.acompletion(**completion_kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/utils.py\", line 1761, in wrapper_async\n    result = await original_function(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/main.py\", line 645, in acompletion\n    response = await _resolve_dispatched_chat_response(init_response)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/main.py\", line 710, in _resolve_dispatched_chat_response\n    return await pending\n           ^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 887, in acompletion\n    headers, response = await self.make_openai_chat_completion_request(\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/litellm_core_utils/logging_utils.py\", line 300, in async_wrapper\n    result: Final = await func(*args, **kwargs)\n                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 422, in make_openai_chat_completion_request\n    raw_response = await openai_aclient.chat.completions.with_raw_response.create(**data, timeout=timeout)\n                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/_legacy_response.py\", line 386, in wrapped\n    return cast(LegacyAPIResponse[R], await func(*args, **kwargs))\n                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/resources/chat/completions/completions.py\", line 2907, in create\n    return await self._post(\n           ^^^^^^^^^^^^^^^^^\n    ...<55 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/_base_client.py\", line 1992, in post\n    return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/_base_client.py\", line 1709, in request\n    response = await self._send_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/_client.py\", line 1097, in _send_request\n    response = await self._send_with_auth_retry(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/_client.py\", line 1075, in _send_with_auth_retry\n    response = await super()._send_request(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/_base_client.py\", line 1628, in _send_request\n    return await self._client.send(request, stream=stream, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/httpx/_client.py\", line 1629, in send\n    response = await self._send_handling_auth(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/httpx/_client.py\", line 1657, in _send_handling_auth\n    response = await self._send_handling_redirects(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/httpx/_client.py\", line 1694, in _send_handling_redirects\n    response = await self._send_single_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/httpx/_client.py\", line 1730, in _send_single_request\n    response = await transport.handle_async_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 389, in handle_async_request\n    response = await self._make_aiohttp_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<6 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 367, in _make_aiohttp_request\n    response: Final = await client_session.request(**request_kwargs).__aenter__()\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/aiohttp/client.py\", line 1693, in __aenter__\n    self._resp: _RetType_co = await self._coro\n                              ^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/aiohttp/client.py\", line 858, in _request\n    resp = await handler(req)\n           ^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/aiohttp/client.py\", line 836, in _connect_and_send_request\n    await resp.start(conn)\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/aiohttp/client_reqrep.py\", line 558, in start\n    message, payload = await protocol.read()  # type: ignore[union-attr]\n                       ^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/aiohttp/streams.py\", line 705, in read\n    await self._waiter\nasyncio.exceptions.CancelledError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 450, in _run_agent_phase\n    await asyncio.wait_for(\n    ...<6 lines>...\n    )\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 487, in wait_for\n    async with timeouts.timeout(timeout):\n               ~~~~~~~~~~~~~~~~^^^^^^^^^\n  File \"/usr/lib64/python3.14/asyncio/timeouts.py\", line 115, in __aexit__\n    raise TimeoutError from exc_val\nTimeoutError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/trial/single_step.py\", line 77, in _run_agent\n    await self._run_agent_phase(\n    ...<4 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 459, in _run_agent_phase\n    raise AgentTimeoutError(\n        f\"Agent execution timed out after {timeout_sec} seconds\"\n    ) from exc\nharbor.trial.errors.AgentTimeoutError: Agent execution timed out after 3600.0 seconds\n",
      "occurred_at": "2026-09-04T17:49:18.708953"
     },
     "outcome": "bestanden",
     "exception_type": "AgentTimeoutError",
     "exception_message": "Agent execution timed out after 3600.0 seconds",
     "episodes": 65,
     "requests": 64,
     "req_max_s": 144,
     "req_mean_s": 31,
     "attempts": 1
    },
    "cobol-modernization": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 576,
     "steps": 13,
     "tokens": {
      "input": 85655,
      "cached": 74688,
      "output": 12707
     },
     "peak_context": 10919,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 13,
     "requests": 13,
     "req_max_s": 142,
     "req_mean_s": 40,
     "attempts": 1
    },
    "configure-git-webserver": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 405,
     "steps": 9,
     "tokens": {
      "input": 39958,
      "cached": 32557,
      "output": 7511
     },
     "peak_context": 7369,
     "exception": null,
     "outcome": "nicht bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 9,
     "requests": 9,
     "req_max_s": 121,
     "req_mean_s": 35,
     "attempts": 1
    },
    "extract-elf": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1613,
     "steps": 14,
     "tokens": {
      "input": 250894,
      "cached": 223161,
      "output": 35183
     },
     "peak_context": 27681,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 14,
     "requests": 14,
     "req_max_s": 353,
     "req_mean_s": 111,
     "attempts": 1
    },
    "fix-git": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 210,
     "steps": 10,
     "tokens": {
      "input": 53111,
      "cached": 45162,
      "output": 3792
     },
     "peak_context": 7913,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 10,
     "requests": 10,
     "req_max_s": 30,
     "req_mean_s": 17,
     "attempts": 1
    },
    "fix-ocaml-gc": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 2473,
     "steps": 36,
     "tokens": {
      "input": 707675,
      "cached": 679800,
      "output": 34572
     },
     "peak_context": 27735,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 36,
     "requests": 36,
     "req_max_s": 324,
     "req_mean_s": 45,
     "attempts": 1
    },
    "git-leak-recovery": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 175,
     "steps": 7,
     "tokens": {
      "input": 26955,
      "cached": 20704,
      "output": 2974
     },
     "peak_context": 6227,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 7,
     "requests": 7,
     "req_max_s": 27,
     "req_mean_s": 18,
     "attempts": 1
    },
    "headless-terminal": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1062,
     "steps": 16,
     "tokens": {
      "input": 170307,
      "cached": 150607,
      "output": 21487
     },
     "peak_context": 19640,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 16,
     "requests": 16,
     "req_max_s": 167,
     "req_mean_s": 53,
     "attempts": 1
    },
    "llm-inference-batching-scheduler": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 3630,
     "steps": 24,
     "tokens": {
      "input": 669401,
      "cached": 601320,
      "output": 68585
     },
     "peak_context": 67989,
     "exception": {
      "exception_type": "AgentTimeoutError",
      "exception_message": "Agent execution timed out after 3600.0 seconds",
      "exception_traceback": "Traceback (most recent call last):\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 488, in wait_for\n    return await fut\n           ^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1607, in run\n    await self._run_agent_loop(\n    ...<3 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1286, in _run_agent_loop\n    ) = await self._handle_llm_interaction(\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, self._session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1164, in _handle_llm_interaction\n    llm_response = await self._query_llm(\n                   ^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1004, in _query_llm\n    llm_response = await chat.chat(\n                   ^^^^^^^^^^^^^^^^\n    ...<2 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/llms/chat.py\", line 89, in chat\n    llm_response: LLMResponse = await self._model.call(\n                                ^^^^^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/llms/lite_llm.py\", line 370, in call\n    response = await litellm.acompletion(**completion_kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/utils.py\", line 1761, in wrapper_async\n    result = await original_function(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/main.py\", line 645, in acompletion\n    response = await _resolve_dispatched_chat_response(init_response)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/main.py\", line 710, in _resolve_dispatched_chat_response\n    return await pending\n           ^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 887, in acompletion\n    headers, response = await self.make_openai_chat_completion_request(\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/litellm_core_utils/logging_utils.py\", line 300, in async_wrapper\n    result: Final = await func(*args, **kwargs)\n                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 422, in make_openai_chat_completion_request\n    raw_response = await openai_aclient.chat.completions.with_raw_response.create(**data, timeout=timeout)\n                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/_legacy_response.py\", line 386, in wrapped\n    return cast(LegacyAPIResponse[R], await func(*args, **kwargs))\n                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/resources/chat/completions/completions.py\", line 2907, in create\n    return await self._post(\n           ^^^^^^^^^^^^^^^^^\n    ...<55 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/_base_client.py\", line 1992, in post\n    return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/_base_client.py\", line 1709, in request\n    response = await self._send_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/_client.py\", line 1097, in _send_request\n    response = await self._send_with_auth_retry(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/_client.py\", line 1075, in _send_with_auth_retry\n    response = await super()._send_request(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/openai/_base_client.py\", line 1628, in _send_request\n    return await self._client.send(request, stream=stream, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/httpx/_client.py\", line 1629, in send\n    response = await self._send_handling_auth(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/httpx/_client.py\", line 1657, in _send_handling_auth\n    response = await self._send_handling_redirects(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/httpx/_client.py\", line 1694, in _send_handling_redirects\n    response = await self._send_single_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/httpx/_client.py\", line 1730, in _send_single_request\n    response = await transport.handle_async_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 389, in handle_async_request\n    response = await self._make_aiohttp_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<6 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 367, in _make_aiohttp_request\n    response: Final = await client_session.request(**request_kwargs).__aenter__()\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/aiohttp/client.py\", line 1693, in __aenter__\n    self._resp: _RetType_co = await self._coro\n                              ^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/aiohttp/client.py\", line 858, in _request\n    resp = await handler(req)\n           ^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/aiohttp/client.py\", line 836, in _connect_and_send_request\n    await resp.start(conn)\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/aiohttp/client_reqrep.py\", line 558, in start\n    message, payload = await protocol.read()  # type: ignore[union-attr]\n                       ^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/aiohttp/streams.py\", line 705, in read\n    await self._waiter\nasyncio.exceptions.CancelledError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 450, in _run_agent_phase\n    await asyncio.wait_for(\n    ...<6 lines>...\n    )\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 487, in wait_for\n    async with timeouts.timeout(timeout):\n               ~~~~~~~~~~~~~~~~^^^^^^^^^\n  File \"/usr/lib64/python3.14/asyncio/timeouts.py\", line 115, in __aexit__\n    raise TimeoutError from exc_val\nTimeoutError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/trial/single_step.py\", line 77, in _run_agent\n    await self._run_agent_phase(\n    ...<4 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/wL2Ply1Y9falsttW/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 459, in _run_agent_phase\n    raise AgentTimeoutError(\n        f\"Agent execution timed out after {timeout_sec} seconds\"\n    ) from exc\nharbor.trial.errors.AgentTimeoutError: Agent execution timed out after 3600.0 seconds\n",
      "occurred_at": "2026-09-04T20:38:38.189907"
     },
     "outcome": "bestanden",
     "exception_type": "AgentTimeoutError",
     "exception_message": "Agent execution timed out after 3600.0 seconds",
     "episodes": 25,
     "requests": 24,
     "req_max_s": 468,
     "req_mean_s": 135,
     "attempts": 1
    },
    "mailman": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 2687,
     "steps": 47,
     "tokens": {
      "input": 1184864,
      "cached": 1138412,
      "output": 36178
     },
     "peak_context": 46268,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 47,
     "requests": 47,
     "req_max_s": 203,
     "req_mean_s": 39,
     "attempts": 1
    },
    "mteb-retrieve": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 816,
     "steps": 13,
     "tokens": {
      "input": 98796,
      "cached": 85917,
      "output": 7036
     },
     "peak_context": 12831,
     "exception": null,
     "outcome": "nicht bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 13,
     "requests": 13,
     "req_max_s": 51,
     "req_mean_s": 23,
     "attempts": 1
    },
    "nginx-request-logging": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 248,
     "steps": 10,
     "tokens": {
      "input": 34851,
      "cached": 29158,
      "output": 4442
     },
     "peak_context": 5657,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 10,
     "requests": 10,
     "req_max_s": 24,
     "req_mean_s": 17,
     "attempts": 1
    },
    "openssl-selfsigned-cert": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 228,
     "steps": 6,
     "tokens": {
      "input": 27514,
      "cached": 19991,
      "output": 4230
     },
     "peak_context": 7503,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 6,
     "requests": 6,
     "req_max_s": 36,
     "req_mean_s": 26,
     "attempts": 1
    },
    "overfull-hbox": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1275,
     "steps": 14,
     "tokens": {
      "input": 118120,
      "cached": 104832,
      "output": 24436
     },
     "peak_context": 13236,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 14,
     "requests": 14,
     "req_max_s": 403,
     "req_mean_s": 72,
     "attempts": 1
    },
    "pypi-server": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 233,
     "steps": 7,
     "tokens": {
      "input": 21337,
      "cached": 16588,
      "output": 2940
     },
     "peak_context": 4725,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 7,
     "requests": 7,
     "req_max_s": 34,
     "req_mean_s": 16,
     "attempts": 1
    },
    "regex-log": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1395,
     "steps": 4,
     "tokens": {
      "input": 16105,
      "cached": 11253,
      "output": 19737
     },
     "peak_context": 5794,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 4,
     "requests": 4,
     "req_max_s": 1146,
     "req_mean_s": 328,
     "attempts": 1
    },
    "sparql-university": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 921,
     "steps": 11,
     "tokens": {
      "input": 84509,
      "cached": 72298,
      "output": 19202
     },
     "peak_context": 12171,
     "exception": null,
     "outcome": "nicht bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 11,
     "requests": 11,
     "req_max_s": 172,
     "req_mean_s": 63,
     "attempts": 1
    },
    "sqlite-with-gcov": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 502,
     "steps": 17,
     "tokens": {
      "input": 105313,
      "cached": 94450,
      "output": 5812
     },
     "peak_context": 10799,
     "exception": null,
     "outcome": "nicht bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 17,
     "requests": 17,
     "req_max_s": 32,
     "req_mean_s": 15,
     "attempts": 1
    }
   }
  },
  {
   "quant": "UD-Q4_K_XL",
   "inference_profile": "mtp4-ngram-thinking-medium",
   "engine": "llama.cpp",
   "engine_version": "0.3.0-dev (build 1, commit 60bce1a)",
   "backend": "rocm",
   "backend_version": "7.1.52802",
   "platform": "AMD Ryzen AI MAX+ 395 (Strix Halo)",
   "model": "Qwen3.8-Flash-Next",
   "n_ctx": 163840,
   "benchmark": "Terminal-Bench-Local",
   "tb_version": "2.1",
   "tb_revision": "5c8eadf1f393183288fa08b8f73ca9a469cc5e00",
   "harbor_version": "0.20.0",
   "agent_timeout_s": 3600,
   "generated_at": "2026-09-04T20:57:22.816805+00:00",
   "total_tasks": 1,
   "passed_tasks": 1,
   "pass_rate": 1.0,
   "duration_s": 114,
   "tokens": {
    "input": 15691,
    "cached": 12125,
    "output": 1923
   },
   "dir": "state/quality/tbench/strix-halo/qwen3.8-flash-da666201-llama.cpp-rocm-UD-Q4_K_XL-mtp4-ngram-thinking-me_results",
   "per_task": {
    "git-leak-recovery": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 114,
     "steps": 7,
     "tokens": {
      "input": 15691,
      "cached": 12125,
      "output": 1923
     },
     "peak_context": 3542,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 7,
     "requests": 7,
     "req_max_s": 13,
     "req_mean_s": 11,
     "attempts": 1
    }
   }
  }
 ],
 "commands": {
  "UD-IQ1_M": {
   "log": "state/quality/tbmini-UD-IQ1_M.log",
   "server_log": "state/logs/tbench-server-20260904-225745.log",
   "command": "ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/38bb39ee97821de2c9009abb7e93950eec396e66/UD-IQ1_M/Qwen3.8-Flash-Next-UD-IQ1_M-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{\"reasoning_effort\": \"medium\"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4",
   "server": {
    "requests": 1,
    "prompt_tokens": 837,
    "generated_tokens": 244,
    "pp_tps": 246.3,
    "tg_tps": 43.4,
    "draft_accept": 0.815,
    "draft_mean_len": 3.79,
    "load_s": 16
   },
   "memory": [
    [
     "Gewichte (resident)",
     "45.2 GiB"
    ],
    [
     "PLE-Tabelle lazy (nicht resident)",
     "26.8 GiB"
    ],
    [
     "KV-Cache (12 Attn-Layer)",
     "2.0 GiB"
    ],
    [
     "Indexer-Cache",
     "0.7 GiB"
    ],
    [
     "DeltaNet-Zustand",
     "0.1 GiB"
    ],
    [
     "Compute-Buffer (Schätzung)",
     "1.6 GiB"
    ],
    [
     "MTP-Head + Draft-KV",
     "3.4 GiB"
    ],
    [
     "Prompt-Cache (max)",
     "2.0 GiB"
    ],
    [
     "Summe",
     "55.1 GiB"
    ],
    [
     "Verfügbar (MemAvailable)",
     "106.5 GiB"
    ],
    [
     "Reserve OS/Page-Cache",
     "6.0 GiB"
    ],
    [
     "Spielraum",
     "45.4 GiB"
    ]
   ],
   "ctx_total": 163840,
   "ctx_per_slot": 163840,
   "slots": 1,
   "apt_mirror": "ftp.fau.de (131.188.12.211)"
  },
  "UD-Q2_K_XL": {
   "log": "state/quality/tbmini-UD-Q2_K_XL.log",
   "server_log": "state/logs/tbench-server-20260904-152101.log",
   "command": "ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-Q2_K_XL/Qwen3.8-Flash-Next-UD-Q2_K_XL-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{\"reasoning_effort\": \"medium\"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4",
   "server": {
    "requests": 399,
    "prompt_tokens": 404631,
    "generated_tokens": 385970,
    "pp_tps": 243.4,
    "tg_tps": 24.4,
    "draft_accept": 0.67,
    "draft_mean_len": 3.48,
    "load_s": 17
   },
   "memory": [
    [
     "Gewichte (resident)",
     "49.2 GiB"
    ],
    [
     "PLE-Tabelle lazy (nicht resident)",
     "26.8 GiB"
    ],
    [
     "KV-Cache (12 Attn-Layer)",
     "2.0 GiB"
    ],
    [
     "Indexer-Cache",
     "0.7 GiB"
    ],
    [
     "DeltaNet-Zustand",
     "0.1 GiB"
    ],
    [
     "Compute-Buffer (Schätzung)",
     "1.6 GiB"
    ],
    [
     "MTP-Head + Draft-KV",
     "3.4 GiB"
    ],
    [
     "Prompt-Cache (max)",
     "2.0 GiB"
    ],
    [
     "Summe",
     "59.2 GiB"
    ],
    [
     "Verfügbar (MemAvailable)",
     "106.5 GiB"
    ],
    [
     "Reserve OS/Page-Cache",
     "6.0 GiB"
    ],
    [
     "Spielraum",
     "41.4 GiB"
    ]
   ],
   "ctx_total": 163840,
   "ctx_per_slot": 163840,
   "slots": 1,
   "apt_mirror": "ftp.fau.de (131.188.12.211)"
  }
 },
 "quant_facts": {
  "UD-Q2_K_XL": {
   "file_gib": 73.4,
   "kld": 0.2246,
   "top1": 82.7,
   "footprint_gib": 59.2
  },
  "UD-IQ3_XXS": {
   "file_gib": 76.3,
   "kld": 0.1651,
   "top1": 85.4,
   "footprint_gib": 62.0
  },
  "UD-IQ4_XS": {
   "file_gib": 87.2,
   "kld": 0.0836,
   "top1": 89.6,
   "footprint_gib": 72.9
  },
  "UD-Q4_K_XL": {
   "file_gib": 103.7,
   "kld": 0.0469,
   "top1": 92.3,
   "footprint_gib": 92.3
  }
 }
};
