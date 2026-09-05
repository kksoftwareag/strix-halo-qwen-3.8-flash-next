window.TBMINI = {
 "generated_at": "2026-09-05T19:13:16+00:00",
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
   "quant": "UD-IQ1_M",
   "inference_profile": "mtp4-ngram-thinking-medium",
   "effort": "medium",
   "label": "UD-IQ1_M · medium",
   "log_key": "UD-IQ1_M",
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
   "generated_at": "2026-09-05T18:42:15.920958+00:00",
   "total_tasks": 20,
   "passed_tasks": 15,
   "pass_rate": 0.75,
   "duration_s": 29780,
   "tokens": {
    "input": 5591475,
    "cached": 5258663,
    "output": 459008
   },
   "dir": "state/quality/tbench/strix-halo/qwen3.8-flash-da666201-llama.cpp-rocm-UD-IQ1_M-mtp4-ngram-thinking-medi_results",
   "per_task": {
    "break-filter-js-from-html": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1250,
     "steps": 9,
     "tokens": {
      "input": 26242,
      "cached": 23292,
      "output": 12383
     },
     "peak_context": 4173,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 9,
     "requests": 9,
     "model_s": 1090,
     "tok_per_s": 11.4,
     "req_max_s": 726,
     "req_mean_s": 121,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/break-filter-js-from-html.json"
    },
    "build-cython-ext": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 2111,
     "steps": 46,
     "tokens": {
      "input": 1370523,
      "cached": 1320525,
      "output": 31057
     },
     "peak_context": 49818,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 46,
     "requests": 46,
     "model_s": 1377,
     "tok_per_s": 22.6,
     "req_max_s": 158,
     "req_mean_s": 30,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/build-cython-ext.json"
    },
    "build-pov-ray": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 2538,
     "steps": 46,
     "tokens": {
      "input": 1180926,
      "cached": 1134091,
      "output": 21483
     },
     "peak_context": 46655,
     "exception": null,
     "outcome": "nicht bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 46,
     "requests": 46,
     "model_s": 1100,
     "tok_per_s": 19.5,
     "req_max_s": 104,
     "req_mean_s": 24,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/build-pov-ray.json"
    },
    "cobol-modernization": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 990,
     "steps": 18,
     "tokens": {
      "input": 164846,
      "cached": 149783,
      "output": 23640
     },
     "peak_context": 14995,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 18,
     "requests": 18,
     "model_s": 939,
     "tok_per_s": 25.2,
     "req_max_s": 312,
     "req_mean_s": 52,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/cobol-modernization.json"
    },
    "configure-git-webserver": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 650,
     "steps": 18,
     "tokens": {
      "input": 126298,
      "cached": 112975,
      "output": 11223
     },
     "peak_context": 13255,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 18,
     "requests": 18,
     "model_s": 455,
     "tok_per_s": 24.7,
     "req_max_s": 46,
     "req_mean_s": 25,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/configure-git-webserver.json"
    },
    "extract-elf": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 3629,
     "steps": 24,
     "tokens": {
      "input": 310161,
      "cached": 282250,
      "output": 76386
     },
     "peak_context": 27819,
     "exception": {
      "exception_type": "AgentTimeoutError",
      "exception_message": "Agent execution timed out after 3600.0 seconds",
      "exception_traceback": "Traceback (most recent call last):\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 488, in wait_for\n    return await fut\n           ^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1607, in run\n    await self._run_agent_loop(\n    ...<3 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1286, in _run_agent_loop\n    ) = await self._handle_llm_interaction(\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, self._session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1164, in _handle_llm_interaction\n    llm_response = await self._query_llm(\n                   ^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1004, in _query_llm\n    llm_response = await chat.chat(\n                   ^^^^^^^^^^^^^^^^\n    ...<2 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/llms/chat.py\", line 89, in chat\n    llm_response: LLMResponse = await self._model.call(\n                                ^^^^^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/llms/lite_llm.py\", line 370, in call\n    response = await litellm.acompletion(**completion_kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/utils.py\", line 1761, in wrapper_async\n    result = await original_function(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/main.py\", line 645, in acompletion\n    response = await _resolve_dispatched_chat_response(init_response)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/main.py\", line 710, in _resolve_dispatched_chat_response\n    return await pending\n           ^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 887, in acompletion\n    headers, response = await self.make_openai_chat_completion_request(\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/litellm_core_utils/logging_utils.py\", line 300, in async_wrapper\n    result: Final = await func(*args, **kwargs)\n                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 422, in make_openai_chat_completion_request\n    raw_response = await openai_aclient.chat.completions.with_raw_response.create(**data, timeout=timeout)\n                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_legacy_response.py\", line 386, in wrapped\n    return cast(LegacyAPIResponse[R], await func(*args, **kwargs))\n                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/resources/chat/completions/completions.py\", line 2907, in create\n    return await self._post(\n           ^^^^^^^^^^^^^^^^^\n    ...<55 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1992, in post\n    return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1709, in request\n    response = await self._send_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_client.py\", line 1097, in _send_request\n    response = await self._send_with_auth_retry(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_client.py\", line 1075, in _send_with_auth_retry\n    response = await super()._send_request(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1628, in _send_request\n    return await self._client.send(request, stream=stream, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1629, in send\n    response = await self._send_handling_auth(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1657, in _send_handling_auth\n    response = await self._send_handling_redirects(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1694, in _send_handling_redirects\n    response = await self._send_single_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1730, in _send_single_request\n    response = await transport.handle_async_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 389, in handle_async_request\n    response = await self._make_aiohttp_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<6 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 367, in _make_aiohttp_request\n    response: Final = await client_session.request(**request_kwargs).__aenter__()\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 1693, in __aenter__\n    self._resp: _RetType_co = await self._coro\n                              ^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 858, in _request\n    resp = await handler(req)\n           ^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 836, in _connect_and_send_request\n    await resp.start(conn)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client_reqrep.py\", line 558, in start\n    message, payload = await protocol.read()  # type: ignore[union-attr]\n                       ^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/streams.py\", line 705, in read\n    await self._waiter\nasyncio.exceptions.CancelledError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 450, in _run_agent_phase\n    await asyncio.wait_for(\n    ...<6 lines>...\n    )\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 487, in wait_for\n    async with timeouts.timeout(timeout):\n               ~~~~~~~~~~~~~~~~^^^^^^^^^\n  File \"/usr/lib64/python3.14/asyncio/timeouts.py\", line 115, in __aexit__\n    raise TimeoutError from exc_val\nTimeoutError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/single_step.py\", line 77, in _run_agent\n    await self._run_agent_phase(\n    ...<4 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 459, in _run_agent_phase\n    raise AgentTimeoutError(\n        f\"Agent execution timed out after {timeout_sec} seconds\"\n    ) from exc\nharbor.trial.errors.AgentTimeoutError: Agent execution timed out after 3600.0 seconds\n",
      "occurred_at": "2026-09-05T02:03:57.217235"
     },
     "outcome": "Zeitlimit",
     "exception_type": "AgentTimeoutError",
     "exception_message": "Agent execution timed out after 3600.0 seconds",
     "episodes": 25,
     "requests": 24,
     "model_s": 3279,
     "tok_per_s": 23.3,
     "req_max_s": 535,
     "req_mean_s": 137,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/extract-elf.json"
    },
    "fix-git": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 271,
     "steps": 10,
     "tokens": {
      "input": 52033,
      "cached": 41962,
      "output": 5297
     },
     "peak_context": 10035,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 10,
     "requests": 10,
     "model_s": 229,
     "tok_per_s": 23.1,
     "req_max_s": 83,
     "req_mean_s": 23,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/fix-git.json"
    },
    "fix-ocaml-gc": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 2307,
     "steps": 29,
     "tokens": {
      "input": 338377,
      "cached": 319666,
      "output": 36704
     },
     "peak_context": 18599,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 29,
     "requests": 29,
     "model_s": 1501,
     "tok_per_s": 24.5,
     "req_max_s": 347,
     "req_mean_s": 52,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/fix-ocaml-gc.json"
    },
    "git-leak-recovery": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 145,
     "steps": 7,
     "tokens": {
      "input": 18298,
      "cached": 14146,
      "output": 2552
     },
     "peak_context": 4128,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 7,
     "requests": 7,
     "model_s": 100,
     "tok_per_s": 25.4,
     "req_max_s": 20,
     "req_mean_s": 14,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/git-leak-recovery.json"
    },
    "headless-terminal": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 588,
     "steps": 15,
     "tokens": {
      "input": 95355,
      "cached": 82748,
      "output": 10842
     },
     "peak_context": 12551,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 15,
     "requests": 15,
     "model_s": 449,
     "tok_per_s": 24.1,
     "req_max_s": 63,
     "req_mean_s": 30,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/headless-terminal.json"
    },
    "llm-inference-batching-scheduler": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 3630,
     "steps": 14,
     "tokens": {
      "input": 157745,
      "cached": 139196,
      "output": 67399
     },
     "peak_context": 19836,
     "exception": {
      "exception_type": "AgentTimeoutError",
      "exception_message": "Agent execution timed out after 3600.0 seconds",
      "exception_traceback": "Traceback (most recent call last):\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 488, in wait_for\n    return await fut\n           ^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1607, in run\n    await self._run_agent_loop(\n    ...<3 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1286, in _run_agent_loop\n    ) = await self._handle_llm_interaction(\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, self._session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1164, in _handle_llm_interaction\n    llm_response = await self._query_llm(\n                   ^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1004, in _query_llm\n    llm_response = await chat.chat(\n                   ^^^^^^^^^^^^^^^^\n    ...<2 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/llms/chat.py\", line 89, in chat\n    llm_response: LLMResponse = await self._model.call(\n                                ^^^^^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/llms/lite_llm.py\", line 370, in call\n    response = await litellm.acompletion(**completion_kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/utils.py\", line 1761, in wrapper_async\n    result = await original_function(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/main.py\", line 645, in acompletion\n    response = await _resolve_dispatched_chat_response(init_response)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/main.py\", line 710, in _resolve_dispatched_chat_response\n    return await pending\n           ^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 887, in acompletion\n    headers, response = await self.make_openai_chat_completion_request(\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/litellm_core_utils/logging_utils.py\", line 300, in async_wrapper\n    result: Final = await func(*args, **kwargs)\n                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 422, in make_openai_chat_completion_request\n    raw_response = await openai_aclient.chat.completions.with_raw_response.create(**data, timeout=timeout)\n                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_legacy_response.py\", line 386, in wrapped\n    return cast(LegacyAPIResponse[R], await func(*args, **kwargs))\n                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/resources/chat/completions/completions.py\", line 2907, in create\n    return await self._post(\n           ^^^^^^^^^^^^^^^^^\n    ...<55 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1992, in post\n    return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1709, in request\n    response = await self._send_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_client.py\", line 1097, in _send_request\n    response = await self._send_with_auth_retry(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_client.py\", line 1075, in _send_with_auth_retry\n    response = await super()._send_request(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1628, in _send_request\n    return await self._client.send(request, stream=stream, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1629, in send\n    response = await self._send_handling_auth(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1657, in _send_handling_auth\n    response = await self._send_handling_redirects(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1694, in _send_handling_redirects\n    response = await self._send_single_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1730, in _send_single_request\n    response = await transport.handle_async_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 389, in handle_async_request\n    response = await self._make_aiohttp_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<6 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 367, in _make_aiohttp_request\n    response: Final = await client_session.request(**request_kwargs).__aenter__()\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 1693, in __aenter__\n    self._resp: _RetType_co = await self._coro\n                              ^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 858, in _request\n    resp = await handler(req)\n           ^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 836, in _connect_and_send_request\n    await resp.start(conn)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client_reqrep.py\", line 558, in start\n    message, payload = await protocol.read()  # type: ignore[union-attr]\n                       ^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/streams.py\", line 705, in read\n    await self._waiter\nasyncio.exceptions.CancelledError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 450, in _run_agent_phase\n    await asyncio.wait_for(\n    ...<6 lines>...\n    )\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 487, in wait_for\n    async with timeouts.timeout(timeout):\n               ~~~~~~~~~~~~~~~~^^^^^^^^^\n  File \"/usr/lib64/python3.14/asyncio/timeouts.py\", line 115, in __aexit__\n    raise TimeoutError from exc_val\nTimeoutError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/single_step.py\", line 77, in _run_agent\n    await self._run_agent_phase(\n    ...<4 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 459, in _run_agent_phase\n    raise AgentTimeoutError(\n        f\"Agent execution timed out after {timeout_sec} seconds\"\n    ) from exc\nharbor.trial.errors.AgentTimeoutError: Agent execution timed out after 3600.0 seconds\n",
      "occurred_at": "2026-09-05T03:59:40.980021"
     },
     "outcome": "Zeitlimit",
     "exception_type": "AgentTimeoutError",
     "exception_message": "Agent execution timed out after 3600.0 seconds",
     "episodes": 15,
     "requests": 14,
     "model_s": 3526,
     "tok_per_s": 19.1,
     "req_max_s": 674,
     "req_mean_s": 252,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/llm-inference-batching-scheduler.json"
    },
    "mailman": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 2805,
     "steps": 42,
     "tokens": {
      "input": 1112405,
      "cached": 1068374,
      "output": 50609
     },
     "peak_context": 43867,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 42,
     "requests": 42,
     "model_s": 2408,
     "tok_per_s": 21.0,
     "req_max_s": 470,
     "req_mean_s": 57,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/mailman.json"
    },
    "mteb-retrieve": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 1019,
     "steps": 19,
     "tokens": {
      "input": 208464,
      "cached": 188525,
      "output": 13298
     },
     "peak_context": 19867,
     "exception": null,
     "outcome": "nicht bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 19,
     "requests": 19,
     "model_s": 538,
     "tok_per_s": 24.7,
     "req_max_s": 100,
     "req_mean_s": 28,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/mteb-retrieve.json"
    },
    "nginx-request-logging": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 152,
     "steps": 6,
     "tokens": {
      "input": 15191,
      "cached": 11644,
      "output": 2432
     },
     "peak_context": 3527,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 6,
     "requests": 6,
     "model_s": 83,
     "tok_per_s": 29.2,
     "req_max_s": 21,
     "req_mean_s": 14,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/nginx-request-logging.json"
    },
    "openssl-selfsigned-cert": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 189,
     "steps": 5,
     "tokens": {
      "input": 18075,
      "cached": 12819,
      "output": 4323
     },
     "peak_context": 5240,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 5,
     "requests": 5,
     "model_s": 144,
     "tok_per_s": 30.1,
     "req_max_s": 66,
     "req_mean_s": 29,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/openssl-selfsigned-cert.json"
    },
    "overfull-hbox": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1286,
     "steps": 16,
     "tokens": {
      "input": 168220,
      "cached": 153292,
      "output": 30863
     },
     "peak_context": 14868,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 16,
     "requests": 16,
     "model_s": 1178,
     "tok_per_s": 26.2,
     "req_max_s": 175,
     "req_mean_s": 74,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/overfull-hbox.json"
    },
    "pypi-server": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 188,
     "steps": 6,
     "tokens": {
      "input": 20385,
      "cached": 15281,
      "output": 2517
     },
     "peak_context": 5084,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 6,
     "requests": 6,
     "model_s": 100,
     "tok_per_s": 25.2,
     "req_max_s": 28,
     "req_mean_s": 17,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/pypi-server.json"
    },
    "regex-log": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 3647,
     "steps": 1,
     "tokens": {
      "input": 960,
      "cached": 956,
      "output": 15802
     },
     "peak_context": 960,
     "exception": {
      "exception_type": "AgentTimeoutError",
      "exception_message": "Agent execution timed out after 3600.0 seconds",
      "exception_traceback": "Traceback (most recent call last):\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 488, in wait_for\n    return await fut\n           ^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1607, in run\n    await self._run_agent_loop(\n    ...<3 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1286, in _run_agent_loop\n    ) = await self._handle_llm_interaction(\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, self._session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1164, in _handle_llm_interaction\n    llm_response = await self._query_llm(\n                   ^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1004, in _query_llm\n    llm_response = await chat.chat(\n                   ^^^^^^^^^^^^^^^^\n    ...<2 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/llms/chat.py\", line 89, in chat\n    llm_response: LLMResponse = await self._model.call(\n                                ^^^^^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/llms/lite_llm.py\", line 370, in call\n    response = await litellm.acompletion(**completion_kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/utils.py\", line 1761, in wrapper_async\n    result = await original_function(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/main.py\", line 645, in acompletion\n    response = await _resolve_dispatched_chat_response(init_response)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/main.py\", line 710, in _resolve_dispatched_chat_response\n    return await pending\n           ^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 887, in acompletion\n    headers, response = await self.make_openai_chat_completion_request(\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/litellm_core_utils/logging_utils.py\", line 300, in async_wrapper\n    result: Final = await func(*args, **kwargs)\n                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 422, in make_openai_chat_completion_request\n    raw_response = await openai_aclient.chat.completions.with_raw_response.create(**data, timeout=timeout)\n                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_legacy_response.py\", line 386, in wrapped\n    return cast(LegacyAPIResponse[R], await func(*args, **kwargs))\n                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/resources/chat/completions/completions.py\", line 2907, in create\n    return await self._post(\n           ^^^^^^^^^^^^^^^^^\n    ...<55 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1992, in post\n    return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1709, in request\n    response = await self._send_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_client.py\", line 1097, in _send_request\n    response = await self._send_with_auth_retry(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_client.py\", line 1075, in _send_with_auth_retry\n    response = await super()._send_request(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1628, in _send_request\n    return await self._client.send(request, stream=stream, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1629, in send\n    response = await self._send_handling_auth(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1657, in _send_handling_auth\n    response = await self._send_handling_redirects(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1694, in _send_handling_redirects\n    response = await self._send_single_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1730, in _send_single_request\n    response = await transport.handle_async_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 389, in handle_async_request\n    response = await self._make_aiohttp_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<6 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 367, in _make_aiohttp_request\n    response: Final = await client_session.request(**request_kwargs).__aenter__()\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 1693, in __aenter__\n    self._resp: _RetType_co = await self._coro\n                              ^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 858, in _request\n    resp = await handler(req)\n           ^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 836, in _connect_and_send_request\n    await resp.start(conn)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client_reqrep.py\", line 558, in start\n    message, payload = await protocol.read()  # type: ignore[union-attr]\n                       ^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/streams.py\", line 705, in read\n    await self._waiter\nasyncio.exceptions.CancelledError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 450, in _run_agent_phase\n    await asyncio.wait_for(\n    ...<6 lines>...\n    )\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 487, in wait_for\n    async with timeouts.timeout(timeout):\n               ~~~~~~~~~~~~~~~~^^^^^^^^^\n  File \"/usr/lib64/python3.14/asyncio/timeouts.py\", line 115, in __aexit__\n    raise TimeoutError from exc_val\nTimeoutError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/single_step.py\", line 77, in _run_agent\n    await self._run_agent_phase(\n    ...<4 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 459, in _run_agent_phase\n    raise AgentTimeoutError(\n        f\"Agent execution timed out after {timeout_sec} seconds\"\n    ) from exc\nharbor.trial.errors.AgentTimeoutError: Agent execution timed out after 3600.0 seconds\n",
      "occurred_at": "2026-09-05T06:34:17.238562"
     },
     "outcome": "Zeitlimit",
     "exception_type": "AgentTimeoutError",
     "exception_message": "Agent execution timed out after 3600.0 seconds",
     "episodes": 2,
     "requests": 1,
     "model_s": 2951,
     "tok_per_s": 5.4,
     "req_max_s": 2951,
     "req_mean_s": 2951,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/regex-log.json"
    },
    "sparql-university": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 2050,
     "steps": 18,
     "tokens": {
      "input": 165844,
      "cached": 152125,
      "output": 36803
     },
     "peak_context": 15350,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 18,
     "requests": 18,
     "model_s": 1859,
     "tok_per_s": 19.8,
     "req_max_s": 1175,
     "req_mean_s": 103,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/sparql-university.json"
    },
    "sqlite-with-gcov": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 334,
     "steps": 12,
     "tokens": {
      "input": 41127,
      "cached": 35013,
      "output": 3395
     },
     "peak_context": 6070,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 12,
     "requests": 12,
     "model_s": 142,
     "tok_per_s": 24.0,
     "req_max_s": 17,
     "req_mean_s": 12,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ1_M-medium/sqlite-with-gcov.json"
    }
   }
  },
  {
   "quant": "UD-Q2_K_XL",
   "inference_profile": "mtp4-ngram-thinking-medium",
   "effort": "medium",
   "label": "UD-Q2_K_XL · medium",
   "log_key": "UD-Q2_K_XL",
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
   "generated_at": "2026-09-05T18:42:15.928180+00:00",
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
     "model_s": 3322,
     "tok_per_s": 6.5,
     "req_max_s": 1839,
     "req_mean_s": 277,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/break-filter-js-from-html.json"
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
     "model_s": 926,
     "tok_per_s": 20.4,
     "req_max_s": 61,
     "req_mean_s": 14,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/build-cython-ext.json"
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
     "model_s": 1988,
     "tok_per_s": 17.4,
     "req_max_s": 144,
     "req_mean_s": 31,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/build-pov-ray.json"
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
     "model_s": 526,
     "tok_per_s": 24.2,
     "req_max_s": 142,
     "req_mean_s": 40,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/cobol-modernization.json"
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
     "model_s": 317,
     "tok_per_s": 23.7,
     "req_max_s": 121,
     "req_mean_s": 35,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/configure-git-webserver.json"
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
     "model_s": 1553,
     "tok_per_s": 22.7,
     "req_max_s": 353,
     "req_mean_s": 111,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/extract-elf.json"
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
     "model_s": 168,
     "tok_per_s": 22.6,
     "req_max_s": 30,
     "req_mean_s": 17,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/fix-git.json"
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
     "model_s": 1630,
     "tok_per_s": 21.2,
     "req_max_s": 324,
     "req_mean_s": 45,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/fix-ocaml-gc.json"
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
     "model_s": 126,
     "tok_per_s": 23.6,
     "req_max_s": 27,
     "req_mean_s": 18,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/git-leak-recovery.json"
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
     "model_s": 853,
     "tok_per_s": 25.2,
     "req_max_s": 167,
     "req_mean_s": 53,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/headless-terminal.json"
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
     "model_s": 3249,
     "tok_per_s": 21.1,
     "req_max_s": 468,
     "req_mean_s": 135,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/llm-inference-batching-scheduler.json"
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
     "model_s": 1833,
     "tok_per_s": 19.7,
     "req_max_s": 203,
     "req_mean_s": 39,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/mailman.json"
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
     "model_s": 294,
     "tok_per_s": 23.9,
     "req_max_s": 51,
     "req_mean_s": 23,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/mteb-retrieve.json"
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
     "model_s": 174,
     "tok_per_s": 25.6,
     "req_max_s": 24,
     "req_mean_s": 17,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/nginx-request-logging.json"
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
     "model_s": 154,
     "tok_per_s": 27.5,
     "req_max_s": 36,
     "req_mean_s": 26,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/openssl-selfsigned-cert.json"
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
     "model_s": 1006,
     "tok_per_s": 24.3,
     "req_max_s": 403,
     "req_mean_s": 72,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/overfull-hbox.json"
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
     "model_s": 115,
     "tok_per_s": 25.6,
     "req_max_s": 34,
     "req_mean_s": 16,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/pypi-server.json"
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
     "model_s": 1312,
     "tok_per_s": 15.0,
     "req_max_s": 1146,
     "req_mean_s": 328,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/regex-log.json"
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
     "model_s": 693,
     "tok_per_s": 27.7,
     "req_max_s": 172,
     "req_mean_s": 63,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/sparql-university.json"
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
     "model_s": 262,
     "tok_per_s": 22.2,
     "req_max_s": 32,
     "req_mean_s": 15,
     "attempts": 1,
     "transcript": "transcripts/UD-Q2_K_XL-medium/sqlite-with-gcov.json"
    }
   }
  },
  {
   "quant": "UD-IQ3_XXS",
   "inference_profile": "mtp4-ngram-thinking-medium",
   "effort": "medium",
   "label": "UD-IQ3_XXS · medium",
   "log_key": "UD-IQ3_XXS",
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
   "generated_at": "2026-09-05T18:42:15.923473+00:00",
   "total_tasks": 20,
   "passed_tasks": 15,
   "pass_rate": 0.75,
   "duration_s": 23236,
   "tokens": {
    "input": 3881359,
    "cached": 3580237,
    "output": 273296
   },
   "dir": "state/quality/tbench/strix-halo/qwen3.8-flash-da666201-llama.cpp-rocm-UD-IQ3_XXS-mtp4-ngram-thinking-me_results",
   "per_task": {
    "break-filter-js-from-html": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 2120,
     "steps": 10,
     "tokens": {
      "input": 30597,
      "cached": 26503,
      "output": 33309
     },
     "peak_context": 4514,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 10,
     "requests": 10,
     "model_s": 2008,
     "tok_per_s": 16.6,
     "req_max_s": 1049,
     "req_mean_s": 201,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/break-filter-js-from-html.json"
    },
    "build-cython-ext": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 2004,
     "steps": 34,
     "tokens": {
      "input": 1090082,
      "cached": 1039509,
      "output": 21208
     },
     "peak_context": 50441,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 34,
     "requests": 34,
     "model_s": 1037,
     "tok_per_s": 20.4,
     "req_max_s": 147,
     "req_mean_s": 31,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/build-cython-ext.json"
    },
    "build-pov-ray": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 3646,
     "steps": 53,
     "tokens": {
      "input": 1082181,
      "cached": 1030319,
      "output": 29791
     },
     "peak_context": 51654,
     "exception": {
      "exception_type": "AgentTimeoutError",
      "exception_message": "Agent execution timed out after 3600.0 seconds",
      "exception_traceback": "Traceback (most recent call last):\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 488, in wait_for\n    return await fut\n           ^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1607, in run\n    await self._run_agent_loop(\n    ...<3 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1286, in _run_agent_loop\n    ) = await self._handle_llm_interaction(\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, self._session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1164, in _handle_llm_interaction\n    llm_response = await self._query_llm(\n                   ^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1004, in _query_llm\n    llm_response = await chat.chat(\n                   ^^^^^^^^^^^^^^^^\n    ...<2 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/llms/chat.py\", line 89, in chat\n    llm_response: LLMResponse = await self._model.call(\n                                ^^^^^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/llms/lite_llm.py\", line 370, in call\n    response = await litellm.acompletion(**completion_kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/utils.py\", line 1761, in wrapper_async\n    result = await original_function(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/main.py\", line 645, in acompletion\n    response = await _resolve_dispatched_chat_response(init_response)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/main.py\", line 710, in _resolve_dispatched_chat_response\n    return await pending\n           ^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 887, in acompletion\n    headers, response = await self.make_openai_chat_completion_request(\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/litellm_core_utils/logging_utils.py\", line 300, in async_wrapper\n    result: Final = await func(*args, **kwargs)\n                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 422, in make_openai_chat_completion_request\n    raw_response = await openai_aclient.chat.completions.with_raw_response.create(**data, timeout=timeout)\n                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_legacy_response.py\", line 386, in wrapped\n    return cast(LegacyAPIResponse[R], await func(*args, **kwargs))\n                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/resources/chat/completions/completions.py\", line 2907, in create\n    return await self._post(\n           ^^^^^^^^^^^^^^^^^\n    ...<55 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1992, in post\n    return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1709, in request\n    response = await self._send_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_client.py\", line 1097, in _send_request\n    response = await self._send_with_auth_retry(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_client.py\", line 1075, in _send_with_auth_retry\n    response = await super()._send_request(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1628, in _send_request\n    return await self._client.send(request, stream=stream, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1629, in send\n    response = await self._send_handling_auth(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1657, in _send_handling_auth\n    response = await self._send_handling_redirects(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1694, in _send_handling_redirects\n    response = await self._send_single_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1730, in _send_single_request\n    response = await transport.handle_async_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 389, in handle_async_request\n    response = await self._make_aiohttp_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<6 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 367, in _make_aiohttp_request\n    response: Final = await client_session.request(**request_kwargs).__aenter__()\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 1693, in __aenter__\n    self._resp: _RetType_co = await self._coro\n                              ^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 858, in _request\n    resp = await handler(req)\n           ^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 836, in _connect_and_send_request\n    await resp.start(conn)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client_reqrep.py\", line 558, in start\n    message, payload = await protocol.read()  # type: ignore[union-attr]\n                       ^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/streams.py\", line 705, in read\n    await self._waiter\nasyncio.exceptions.CancelledError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 450, in _run_agent_phase\n    await asyncio.wait_for(\n    ...<6 lines>...\n    )\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 487, in wait_for\n    async with timeouts.timeout(timeout):\n               ~~~~~~~~~~~~~~~~^^^^^^^^^\n  File \"/usr/lib64/python3.14/asyncio/timeouts.py\", line 115, in __aexit__\n    raise TimeoutError from exc_val\nTimeoutError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/single_step.py\", line 77, in _run_agent\n    await self._run_agent_phase(\n    ...<4 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 459, in _run_agent_phase\n    raise AgentTimeoutError(\n        f\"Agent execution timed out after {timeout_sec} seconds\"\n    ) from exc\nharbor.trial.errors.AgentTimeoutError: Agent execution timed out after 3600.0 seconds\n",
      "occurred_at": "2026-09-05T09:24:49.580862"
     },
     "outcome": "Zeitlimit",
     "exception_type": "AgentTimeoutError",
     "exception_message": "Agent execution timed out after 3600.0 seconds",
     "episodes": 54,
     "requests": 53,
     "model_s": 1633,
     "tok_per_s": 18.2,
     "req_max_s": 108,
     "req_mean_s": 31,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/build-pov-ray.json"
    },
    "cobol-modernization": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 992,
     "steps": 15,
     "tokens": {
      "input": 162542,
      "cached": 143595,
      "output": 20825
     },
     "peak_context": 18891,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 15,
     "requests": 15,
     "model_s": 900,
     "tok_per_s": 23.1,
     "req_max_s": 246,
     "req_mean_s": 60,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/cobol-modernization.json"
    },
    "configure-git-webserver": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 380,
     "steps": 11,
     "tokens": {
      "input": 108846,
      "cached": 92830,
      "output": 4913
     },
     "peak_context": 15976,
     "exception": null,
     "outcome": "nicht bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 11,
     "requests": 11,
     "model_s": 239,
     "tok_per_s": 20.6,
     "req_max_s": 33,
     "req_mean_s": 22,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/configure-git-webserver.json"
    },
    "extract-elf": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 568,
     "steps": 6,
     "tokens": {
      "input": 28971,
      "cached": 19671,
      "output": 11943
     },
     "peak_context": 9280,
     "exception": null,
     "outcome": "nicht bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 6,
     "requests": 6,
     "model_s": 532,
     "tok_per_s": 22.4,
     "req_max_s": 292,
     "req_mean_s": 89,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/extract-elf.json"
    },
    "fix-git": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 201,
     "steps": 10,
     "tokens": {
      "input": 39324,
      "cached": 32944,
      "output": 3708
     },
     "peak_context": 6344,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 10,
     "requests": 10,
     "model_s": 155,
     "tok_per_s": 23.9,
     "req_max_s": 30,
     "req_mean_s": 16,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/fix-git.json"
    },
    "fix-ocaml-gc": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1923,
     "steps": 27,
     "tokens": {
      "input": 383372,
      "cached": 361022,
      "output": 21810
     },
     "peak_context": 22246,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 27,
     "requests": 27,
     "model_s": 1059,
     "tok_per_s": 20.6,
     "req_max_s": 267,
     "req_mean_s": 39,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/fix-ocaml-gc.json"
    },
    "git-leak-recovery": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 149,
     "steps": 6,
     "tokens": {
      "input": 15732,
      "cached": 11686,
      "output": 2430
     },
     "peak_context": 4026,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 6,
     "requests": 6,
     "model_s": 103,
     "tok_per_s": 23.6,
     "req_max_s": 22,
     "req_mean_s": 17,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/git-leak-recovery.json"
    },
    "headless-terminal": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 410,
     "steps": 8,
     "tokens": {
      "input": 42392,
      "cached": 32432,
      "output": 8630
     },
     "peak_context": 9932,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 8,
     "requests": 8,
     "model_s": 328,
     "tok_per_s": 26.3,
     "req_max_s": 210,
     "req_mean_s": 41,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/headless-terminal.json"
    },
    "llm-inference-batching-scheduler": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 3638,
     "steps": 6,
     "tokens": {
      "input": 33899,
      "cached": 26142,
      "output": 19164
     },
     "peak_context": 9148,
     "exception": {
      "exception_type": "AgentTimeoutError",
      "exception_message": "Agent execution timed out after 3600.0 seconds",
      "exception_traceback": "Traceback (most recent call last):\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 488, in wait_for\n    return await fut\n           ^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1607, in run\n    await self._run_agent_loop(\n    ...<3 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1286, in _run_agent_loop\n    ) = await self._handle_llm_interaction(\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, self._session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1164, in _handle_llm_interaction\n    llm_response = await self._query_llm(\n                   ^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1004, in _query_llm\n    llm_response = await chat.chat(\n                   ^^^^^^^^^^^^^^^^\n    ...<2 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/llms/chat.py\", line 89, in chat\n    llm_response: LLMResponse = await self._model.call(\n                                ^^^^^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/llms/lite_llm.py\", line 370, in call\n    response = await litellm.acompletion(**completion_kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/utils.py\", line 1761, in wrapper_async\n    result = await original_function(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/main.py\", line 645, in acompletion\n    response = await _resolve_dispatched_chat_response(init_response)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/main.py\", line 710, in _resolve_dispatched_chat_response\n    return await pending\n           ^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 887, in acompletion\n    headers, response = await self.make_openai_chat_completion_request(\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/litellm_core_utils/logging_utils.py\", line 300, in async_wrapper\n    result: Final = await func(*args, **kwargs)\n                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 422, in make_openai_chat_completion_request\n    raw_response = await openai_aclient.chat.completions.with_raw_response.create(**data, timeout=timeout)\n                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_legacy_response.py\", line 386, in wrapped\n    return cast(LegacyAPIResponse[R], await func(*args, **kwargs))\n                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/resources/chat/completions/completions.py\", line 2907, in create\n    return await self._post(\n           ^^^^^^^^^^^^^^^^^\n    ...<55 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1992, in post\n    return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1709, in request\n    response = await self._send_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_client.py\", line 1097, in _send_request\n    response = await self._send_with_auth_retry(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_client.py\", line 1075, in _send_with_auth_retry\n    response = await super()._send_request(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/openai/_base_client.py\", line 1628, in _send_request\n    return await self._client.send(request, stream=stream, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1629, in send\n    response = await self._send_handling_auth(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1657, in _send_handling_auth\n    response = await self._send_handling_redirects(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1694, in _send_handling_redirects\n    response = await self._send_single_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/httpx/_client.py\", line 1730, in _send_single_request\n    response = await transport.handle_async_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 389, in handle_async_request\n    response = await self._make_aiohttp_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<6 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 367, in _make_aiohttp_request\n    response: Final = await client_session.request(**request_kwargs).__aenter__()\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 1693, in __aenter__\n    self._resp: _RetType_co = await self._coro\n                              ^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 858, in _request\n    resp = await handler(req)\n           ^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client.py\", line 836, in _connect_and_send_request\n    await resp.start(conn)\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/client_reqrep.py\", line 558, in start\n    message, payload = await protocol.read()  # type: ignore[union-attr]\n                       ^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/aiohttp/streams.py\", line 705, in read\n    await self._waiter\nasyncio.exceptions.CancelledError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 450, in _run_agent_phase\n    await asyncio.wait_for(\n    ...<6 lines>...\n    )\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 487, in wait_for\n    async with timeouts.timeout(timeout):\n               ~~~~~~~~~~~~~~~~^^^^^^^^^\n  File \"/usr/lib64/python3.14/asyncio/timeouts.py\", line 115, in __aexit__\n    raise TimeoutError from exc_val\nTimeoutError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/single_step.py\", line 77, in _run_agent\n    await self._run_agent_phase(\n    ...<4 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/lKAELigiEjYpFnuK/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 459, in _run_agent_phase\n    raise AgentTimeoutError(\n        f\"Agent execution timed out after {timeout_sec} seconds\"\n    ) from exc\nharbor.trial.errors.AgentTimeoutError: Agent execution timed out after 3600.0 seconds\n",
      "occurred_at": "2026-09-05T11:42:37.604172"
     },
     "outcome": "Zeitlimit",
     "exception_type": "AgentTimeoutError",
     "exception_message": "Agent execution timed out after 3600.0 seconds",
     "episodes": 7,
     "requests": 6,
     "model_s": 3143,
     "tok_per_s": 6.1,
     "req_max_s": 2854,
     "req_mean_s": 524,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/llm-inference-batching-scheduler.json"
    },
    "mailman": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1495,
     "steps": 20,
     "tokens": {
      "input": 260123,
      "cached": 240916,
      "output": 15253
     },
     "peak_context": 21762,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 20,
     "requests": 20,
     "model_s": 1278,
     "tok_per_s": 11.9,
     "req_max_s": 651,
     "req_mean_s": 64,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/mailman.json"
    },
    "mteb-retrieve": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 1275,
     "steps": 17,
     "tokens": {
      "input": 165974,
      "cached": 147482,
      "output": 15500
     },
     "peak_context": 18428,
     "exception": null,
     "outcome": "nicht bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 17,
     "requests": 17,
     "model_s": 676,
     "tok_per_s": 22.9,
     "req_max_s": 88,
     "req_mean_s": 40,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/mteb-retrieve.json"
    },
    "nginx-request-logging": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 173,
     "steps": 5,
     "tokens": {
      "input": 13176,
      "cached": 9166,
      "output": 2830
     },
     "peak_context": 3994,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 5,
     "requests": 5,
     "model_s": 104,
     "tok_per_s": 27.3,
     "req_max_s": 29,
     "req_mean_s": 21,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/nginx-request-logging.json"
    },
    "openssl-selfsigned-cert": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 148,
     "steps": 3,
     "tokens": {
      "input": 11092,
      "cached": 5520,
      "output": 2791
     },
     "peak_context": 5564,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 3,
     "requests": 3,
     "model_s": 103,
     "tok_per_s": 27.2,
     "req_max_s": 51,
     "req_mean_s": 34,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/openssl-selfsigned-cert.json"
    },
    "overfull-hbox": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 958,
     "steps": 18,
     "tokens": {
      "input": 174816,
      "cached": 159713,
      "output": 12121
     },
     "peak_context": 15035,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 18,
     "requests": 18,
     "model_s": 578,
     "tok_per_s": 21.0,
     "req_max_s": 153,
     "req_mean_s": 32,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/overfull-hbox.json"
    },
    "pypi-server": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 222,
     "steps": 7,
     "tokens": {
      "input": 23802,
      "cached": 18781,
      "output": 2946
     },
     "peak_context": 4997,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 7,
     "requests": 7,
     "model_s": 123,
     "tok_per_s": 23.9,
     "req_max_s": 30,
     "req_mean_s": 18,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/pypi-server.json"
    },
    "regex-log": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1466,
     "steps": 6,
     "tokens": {
      "input": 32589,
      "cached": 24620,
      "output": 21872
     },
     "peak_context": 8905,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 6,
     "requests": 6,
     "model_s": 1408,
     "tok_per_s": 15.5,
     "req_max_s": 1032,
     "req_mean_s": 235,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/regex-log.json"
    },
    "sparql-university": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1065,
     "steps": 14,
     "tokens": {
      "input": 107190,
      "cached": 96515,
      "output": 19183
     },
     "peak_context": 10623,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 14,
     "requests": 14,
     "model_s": 724,
     "tok_per_s": 26.5,
     "req_max_s": 391,
     "req_mean_s": 52,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/sparql-university.json"
    },
    "sqlite-with-gcov": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 405,
     "steps": 11,
     "tokens": {
      "input": 74659,
      "cached": 60871,
      "output": 3069
     },
     "peak_context": 13748,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 11,
     "requests": 11,
     "model_s": 158,
     "tok_per_s": 19.5,
     "req_max_s": 22,
     "req_mean_s": 14,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ3_XXS-medium/sqlite-with-gcov.json"
    }
   }
  },
  {
   "quant": "UD-IQ4_XS",
   "inference_profile": "mtp4-ngram-thinking-medium",
   "effort": "medium",
   "label": "UD-IQ4_XS · medium",
   "log_key": "UD-IQ4_XS",
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
   "generated_at": "2026-09-05T18:42:15.925762+00:00",
   "total_tasks": 20,
   "passed_tasks": 15,
   "pass_rate": 0.75,
   "duration_s": 25062,
   "tokens": {
    "input": 4218352,
    "cached": 3879148,
    "output": 343555
   },
   "dir": "state/quality/tbench/strix-halo/qwen3.8-flash-da666201-llama.cpp-rocm-UD-IQ4_XS-mtp4-ngram-thinking-med_results",
   "per_task": {
    "break-filter-js-from-html": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1235,
     "steps": 9,
     "tokens": {
      "input": 27901,
      "cached": 23161,
      "output": 27571
     },
     "peak_context": 4708,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 9,
     "requests": 9,
     "model_s": 1152,
     "tok_per_s": 23.9,
     "req_max_s": 550,
     "req_mean_s": 128,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/break-filter-js-from-html.json"
    },
    "build-cython-ext": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1689,
     "steps": 35,
     "tokens": {
      "input": 724394,
      "cached": 687825,
      "output": 19141
     },
     "peak_context": 36433,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 35,
     "requests": 35,
     "model_s": 853,
     "tok_per_s": 22.4,
     "req_max_s": 104,
     "req_mean_s": 24,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/build-cython-ext.json"
    },
    "build-pov-ray": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 3648,
     "steps": 39,
     "tokens": {
      "input": 1210268,
      "cached": 1148882,
      "output": 39876
     },
     "peak_context": 61234,
     "exception": {
      "exception_type": "AgentTimeoutError",
      "exception_message": "Agent execution timed out after 3600.0 seconds",
      "exception_traceback": "Traceback (most recent call last):\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 488, in wait_for\n    return await fut\n           ^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1607, in run\n    await self._run_agent_loop(\n    ...<3 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1286, in _run_agent_loop\n    ) = await self._handle_llm_interaction(\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, self._session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1164, in _handle_llm_interaction\n    llm_response = await self._query_llm(\n                   ^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1004, in _query_llm\n    llm_response = await chat.chat(\n                   ^^^^^^^^^^^^^^^^\n    ...<2 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/llms/chat.py\", line 89, in chat\n    llm_response: LLMResponse = await self._model.call(\n                                ^^^^^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/llms/lite_llm.py\", line 370, in call\n    response = await litellm.acompletion(**completion_kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/utils.py\", line 1761, in wrapper_async\n    result = await original_function(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/main.py\", line 645, in acompletion\n    response = await _resolve_dispatched_chat_response(init_response)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/main.py\", line 710, in _resolve_dispatched_chat_response\n    return await pending\n           ^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 887, in acompletion\n    headers, response = await self.make_openai_chat_completion_request(\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/litellm_core_utils/logging_utils.py\", line 300, in async_wrapper\n    result: Final = await func(*args, **kwargs)\n                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 422, in make_openai_chat_completion_request\n    raw_response = await openai_aclient.chat.completions.with_raw_response.create(**data, timeout=timeout)\n                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/_legacy_response.py\", line 386, in wrapped\n    return cast(LegacyAPIResponse[R], await func(*args, **kwargs))\n                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/resources/chat/completions/completions.py\", line 2907, in create\n    return await self._post(\n           ^^^^^^^^^^^^^^^^^\n    ...<55 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/_base_client.py\", line 1992, in post\n    return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/_base_client.py\", line 1709, in request\n    response = await self._send_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/_client.py\", line 1097, in _send_request\n    response = await self._send_with_auth_retry(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/_client.py\", line 1075, in _send_with_auth_retry\n    response = await super()._send_request(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/_base_client.py\", line 1628, in _send_request\n    return await self._client.send(request, stream=stream, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/httpx/_client.py\", line 1629, in send\n    response = await self._send_handling_auth(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/httpx/_client.py\", line 1657, in _send_handling_auth\n    response = await self._send_handling_redirects(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/httpx/_client.py\", line 1694, in _send_handling_redirects\n    response = await self._send_single_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/httpx/_client.py\", line 1730, in _send_single_request\n    response = await transport.handle_async_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 389, in handle_async_request\n    response = await self._make_aiohttp_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<6 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 367, in _make_aiohttp_request\n    response: Final = await client_session.request(**request_kwargs).__aenter__()\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/aiohttp/client.py\", line 1693, in __aenter__\n    self._resp: _RetType_co = await self._coro\n                              ^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/aiohttp/client.py\", line 858, in _request\n    resp = await handler(req)\n           ^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/aiohttp/client.py\", line 836, in _connect_and_send_request\n    await resp.start(conn)\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/aiohttp/client_reqrep.py\", line 558, in start\n    message, payload = await protocol.read()  # type: ignore[union-attr]\n                       ^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/aiohttp/streams.py\", line 705, in read\n    await self._waiter\nasyncio.exceptions.CancelledError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 450, in _run_agent_phase\n    await asyncio.wait_for(\n    ...<6 lines>...\n    )\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 487, in wait_for\n    async with timeouts.timeout(timeout):\n               ~~~~~~~~~~~~~~~~^^^^^^^^^\n  File \"/usr/lib64/python3.14/asyncio/timeouts.py\", line 115, in __aexit__\n    raise TimeoutError from exc_val\nTimeoutError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/trial/single_step.py\", line 77, in _run_agent\n    await self._run_agent_phase(\n    ...<4 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 459, in _run_agent_phase\n    raise AgentTimeoutError(\n        f\"Agent execution timed out after {timeout_sec} seconds\"\n    ) from exc\nharbor.trial.errors.AgentTimeoutError: Agent execution timed out after 3600.0 seconds\n",
      "occurred_at": "2026-09-05T15:33:32.046898"
     },
     "outcome": "Zeitlimit",
     "exception_type": "AgentTimeoutError",
     "exception_message": "Agent execution timed out after 3600.0 seconds",
     "episodes": 40,
     "requests": 39,
     "model_s": 2236,
     "tok_per_s": 17.8,
     "req_max_s": 195,
     "req_mean_s": 57,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/build-pov-ray.json"
    },
    "cobol-modernization": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 811,
     "steps": 17,
     "tokens": {
      "input": 169614,
      "cached": 151637,
      "output": 17355
     },
     "peak_context": 17913,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 17,
     "requests": 17,
     "model_s": 745,
     "tok_per_s": 23.3,
     "req_max_s": 203,
     "req_mean_s": 44,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/cobol-modernization.json"
    },
    "configure-git-webserver": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 348,
     "steps": 10,
     "tokens": {
      "input": 37375,
      "cached": 30081,
      "output": 5656
     },
     "peak_context": 7258,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 10,
     "requests": 10,
     "model_s": 216,
     "tok_per_s": 26.2,
     "req_max_s": 33,
     "req_mean_s": 22,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/configure-git-webserver.json"
    },
    "extract-elf": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 1052,
     "steps": 10,
     "tokens": {
      "input": 97226,
      "cached": 82067,
      "output": 24558
     },
     "peak_context": 15123,
     "exception": null,
     "outcome": "nicht bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 10,
     "requests": 10,
     "model_s": 1004,
     "tok_per_s": 24.5,
     "req_max_s": 211,
     "req_mean_s": 100,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/extract-elf.json"
    },
    "fix-git": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 177,
     "steps": 9,
     "tokens": {
      "input": 29237,
      "cached": 24117,
      "output": 3302
     },
     "peak_context": 5088,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 9,
     "requests": 9,
     "model_s": 136,
     "tok_per_s": 24.4,
     "req_max_s": 25,
     "req_mean_s": 15,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/fix-git.json"
    },
    "fix-ocaml-gc": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 4930,
     "steps": 29,
     "tokens": {
      "input": 430554,
      "cached": 405575,
      "output": 40257
     },
     "peak_context": 24867,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 29,
     "requests": 29,
     "model_s": 1905,
     "tok_per_s": 21.1,
     "req_max_s": 485,
     "req_mean_s": 66,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/fix-ocaml-gc.json"
    },
    "git-leak-recovery": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 532,
     "steps": 7,
     "tokens": {
      "input": 20186,
      "cached": 15749,
      "output": 2620
     },
     "peak_context": 4413,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 7,
     "requests": 7,
     "model_s": 102,
     "tok_per_s": 25.6,
     "req_max_s": 18,
     "req_mean_s": 15,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/git-leak-recovery.json"
    },
    "headless-terminal": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 519,
     "steps": 13,
     "tokens": {
      "input": 118008,
      "cached": 101480,
      "output": 10844
     },
     "peak_context": 16480,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 13,
     "requests": 13,
     "model_s": 402,
     "tok_per_s": 27.0,
     "req_max_s": 91,
     "req_mean_s": 31,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/headless-terminal.json"
    },
    "llm-inference-batching-scheduler": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 3802,
     "steps": 23,
     "tokens": {
      "input": 657112,
      "cached": 596379,
      "output": 68941
     },
     "peak_context": 60645,
     "exception": {
      "exception_type": "AgentTimeoutError",
      "exception_message": "Agent execution timed out after 3600.0 seconds",
      "exception_traceback": "Traceback (most recent call last):\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 488, in wait_for\n    return await fut\n           ^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1607, in run\n    await self._run_agent_loop(\n    ...<3 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1286, in _run_agent_loop\n    ) = await self._handle_llm_interaction(\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, self._session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1164, in _handle_llm_interaction\n    llm_response = await self._query_llm(\n                   ^^^^^^^^^^^^^^^^^^^^^^\n        chat, prompt, original_instruction, session\n        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/agents/terminus_2/terminus_2.py\", line 1004, in _query_llm\n    llm_response = await chat.chat(\n                   ^^^^^^^^^^^^^^^^\n    ...<2 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/llms/chat.py\", line 89, in chat\n    llm_response: LLMResponse = await self._model.call(\n                                ^^^^^^^^^^^^^^^^^^^^^^^\n    ...<5 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 193, in async_wrapped\n    return await copy(fn, *args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 112, in __call__\n    do = await self.iter(retry_state=retry_state)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 157, in iter\n    result = await action(retry_state)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/_utils.py\", line 111, in inner\n    return call(*args, **kwargs)\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/__init__.py\", line 393, in <lambda>\n    self._add_action_func(lambda rs: rs.outcome.result())\n                                     ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 447, in result\n    return self.__get_result()\n           ~~~~~~~~~~~~~~~~~^^\n  File \"/usr/lib64/python3.14/concurrent/futures/_base.py\", line 396, in __get_result\n    raise self._exception\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/tenacity/asyncio/__init__.py\", line 116, in __call__\n    result = await fn(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/llms/lite_llm.py\", line 370, in call\n    response = await litellm.acompletion(**completion_kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/utils.py\", line 1761, in wrapper_async\n    result = await original_function(*args, **kwargs)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/main.py\", line 645, in acompletion\n    response = await _resolve_dispatched_chat_response(init_response)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/main.py\", line 710, in _resolve_dispatched_chat_response\n    return await pending\n           ^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 887, in acompletion\n    headers, response = await self.make_openai_chat_completion_request(\n                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/litellm_core_utils/logging_utils.py\", line 300, in async_wrapper\n    result: Final = await func(*args, **kwargs)\n                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/llms/openai/openai.py\", line 422, in make_openai_chat_completion_request\n    raw_response = await openai_aclient.chat.completions.with_raw_response.create(**data, timeout=timeout)\n                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/_legacy_response.py\", line 386, in wrapped\n    return cast(LegacyAPIResponse[R], await func(*args, **kwargs))\n                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/resources/chat/completions/completions.py\", line 2907, in create\n    return await self._post(\n           ^^^^^^^^^^^^^^^^^\n    ...<55 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/_base_client.py\", line 1992, in post\n    return await self.request(cast_to, opts, stream=stream, stream_cls=stream_cls)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/_base_client.py\", line 1709, in request\n    response = await self._send_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/_client.py\", line 1097, in _send_request\n    response = await self._send_with_auth_retry(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/_client.py\", line 1075, in _send_with_auth_retry\n    response = await super()._send_request(request, stream=stream, **kwargs)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/openai/_base_client.py\", line 1628, in _send_request\n    return await self._client.send(request, stream=stream, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/httpx/_client.py\", line 1629, in send\n    response = await self._send_handling_auth(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<4 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/httpx/_client.py\", line 1657, in _send_handling_auth\n    response = await self._send_handling_redirects(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<3 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/httpx/_client.py\", line 1694, in _send_handling_redirects\n    response = await self._send_single_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/httpx/_client.py\", line 1730, in _send_single_request\n    response = await transport.handle_async_request(request)\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 389, in handle_async_request\n    response = await self._make_aiohttp_request(\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n    ...<6 lines>...\n    )\n    ^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/litellm/llms/custom_httpx/aiohttp_transport.py\", line 367, in _make_aiohttp_request\n    response: Final = await client_session.request(**request_kwargs).__aenter__()\n                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/aiohttp/client.py\", line 1693, in __aenter__\n    self._resp: _RetType_co = await self._coro\n                              ^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/aiohttp/client.py\", line 858, in _request\n    resp = await handler(req)\n           ^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/aiohttp/client.py\", line 836, in _connect_and_send_request\n    await resp.start(conn)\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/aiohttp/client_reqrep.py\", line 558, in start\n    message, payload = await protocol.read()  # type: ignore[union-attr]\n                       ^^^^^^^^^^^^^^^^^^^^^\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/aiohttp/streams.py\", line 705, in read\n    await self._waiter\nasyncio.exceptions.CancelledError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 450, in _run_agent_phase\n    await asyncio.wait_for(\n    ...<6 lines>...\n    )\n  File \"/usr/lib64/python3.14/asyncio/tasks.py\", line 487, in wait_for\n    async with timeouts.timeout(timeout):\n               ~~~~~~~~~~~~~~~~^^^^^^^^^\n  File \"/usr/lib64/python3.14/asyncio/timeouts.py\", line 115, in __aexit__\n    raise TimeoutError from exc_val\nTimeoutError\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/trial/single_step.py\", line 77, in _run_agent\n    await self._run_agent_phase(\n    ...<4 lines>...\n    )\n  File \"/home/lyra/.cache/uv/archive-v0/L52IIASCTH1OQs0n/lib64/python3.14/site-packages/harbor/trial/trial.py\", line 459, in _run_agent_phase\n    raise AgentTimeoutError(\n        f\"Agent execution timed out after {timeout_sec} seconds\"\n    ) from exc\nharbor.trial.errors.AgentTimeoutError: Agent execution timed out after 3600.0 seconds\n",
      "occurred_at": "2026-09-05T18:53:47.526494"
     },
     "outcome": "Zeitlimit",
     "exception_type": "AgentTimeoutError",
     "exception_message": "Agent execution timed out after 3600.0 seconds",
     "episodes": 24,
     "requests": 23,
     "model_s": 3468,
     "tok_per_s": 19.9,
     "req_max_s": 372,
     "req_mean_s": 151,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/llm-inference-batching-scheduler.json"
    },
    "mailman": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 1298,
     "steps": 18,
     "tokens": {
      "input": 258702,
      "cached": 237490,
      "output": 18734
     },
     "peak_context": 21144,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 18,
     "requests": 18,
     "model_s": 849,
     "tok_per_s": 22.1,
     "req_max_s": 271,
     "req_mean_s": 47,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/mailman.json"
    },
    "mteb-retrieve": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 686,
     "steps": 10,
     "tokens": {
      "input": 51192,
      "cached": 42295,
      "output": 6008
     },
     "peak_context": 8861,
     "exception": null,
     "outcome": "nicht bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 10,
     "requests": 10,
     "model_s": 236,
     "tok_per_s": 25.4,
     "req_max_s": 52,
     "req_mean_s": 24,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/mteb-retrieve.json"
    },
    "nginx-request-logging": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 198,
     "steps": 6,
     "tokens": {
      "input": 31749,
      "cached": 24370,
      "output": 3032
     },
     "peak_context": 7359,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 6,
     "requests": 6,
     "model_s": 115,
     "tok_per_s": 26.5,
     "req_max_s": 32,
     "req_mean_s": 19,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/nginx-request-logging.json"
    },
    "openssl-selfsigned-cert": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 384,
     "steps": 4,
     "tokens": {
      "input": 11607,
      "cached": 7240,
      "output": 3916
     },
     "peak_context": 4355,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 4,
     "requests": 4,
     "model_s": 130,
     "tok_per_s": 30.2,
     "req_max_s": 71,
     "req_mean_s": 32,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/openssl-selfsigned-cert.json"
    },
    "overfull-hbox": {
     "passed": false,
     "reward": 0.0,
     "duration_s": 1193,
     "steps": 17,
     "tokens": {
      "input": 167543,
      "cached": 151778,
      "output": 20455
     },
     "peak_context": 15701,
     "exception": null,
     "outcome": "nicht bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 17,
     "requests": 17,
     "model_s": 925,
     "tok_per_s": 22.1,
     "req_max_s": 208,
     "req_mean_s": 54,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/overfull-hbox.json"
    },
    "pypi-server": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 609,
     "steps": 11,
     "tokens": {
      "input": 45311,
      "cached": 39083,
      "output": 3704
     },
     "peak_context": 6188,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 11,
     "requests": 11,
     "model_s": 148,
     "tok_per_s": 25.0,
     "req_max_s": 23,
     "req_mean_s": 13,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/pypi-server.json"
    },
    "regex-log": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 700,
     "steps": 3,
     "tokens": {
      "input": 8672,
      "cached": 4432,
      "output": 14433
     },
     "peak_context": 4232,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 3,
     "requests": 3,
     "model_s": 517,
     "tok_per_s": 27.9,
     "req_max_s": 410,
     "req_mean_s": 172,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/regex-log.json"
    },
    "sparql-university": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 757,
     "steps": 11,
     "tokens": {
      "input": 63006,
      "cached": 54306,
      "output": 9876
     },
     "peak_context": 8660,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 11,
     "requests": 11,
     "model_s": 396,
     "tok_per_s": 25.0,
     "req_max_s": 217,
     "req_mean_s": 36,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/sparql-university.json"
    },
    "sqlite-with-gcov": {
     "passed": true,
     "reward": 1.0,
     "duration_s": 494,
     "steps": 13,
     "tokens": {
      "input": 58695,
      "cached": 51201,
      "output": 3276
     },
     "peak_context": 7446,
     "exception": null,
     "outcome": "bestanden",
     "exception_type": null,
     "exception_message": null,
     "episodes": 13,
     "requests": 13,
     "model_s": 147,
     "tok_per_s": 22.3,
     "req_max_s": 18,
     "req_mean_s": 11,
     "attempts": 1,
     "transcript": "transcripts/UD-IQ4_XS-medium/sqlite-with-gcov.json"
    }
   }
  },
  {
   "quant": "UD-Q4_K_XL",
   "inference_profile": "mtp4-ngram-thinking-medium",
   "effort": "medium",
   "label": "UD-Q4_K_XL · medium",
   "log_key": "UD-Q4_K_XL",
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
   "generated_at": "2026-09-05T18:42:15.929948+00:00",
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
     "model_s": 74,
     "tok_per_s": 26.0,
     "req_max_s": 13,
     "req_mean_s": 11,
     "attempts": 1,
     "transcript": "transcripts/UD-Q4_K_XL-medium/git-leak-recovery.json"
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
    "requests": 361,
    "prompt_tokens": 332812,
    "generated_tokens": 459008,
    "pp_tps": 216.6,
    "tg_tps": 26.0,
    "draft_accept": 0.683,
    "draft_mean_len": 3.52,
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
  "UD-IQ3_XXS": {
   "log": "state/quality/tbmini-UD-IQ3_XXS.log",
   "server_log": "state/logs/tbench-server-20260905-071456.log",
   "command": "ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-IQ3_XXS/Qwen3.8-Flash-Next-UD-IQ3_XXS-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{\"reasoning_effort\": \"medium\"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4",
   "server": {
    "requests": 287,
    "prompt_tokens": 301122,
    "generated_tokens": 273296,
    "pp_tps": 252.7,
    "tg_tps": 25.1,
    "draft_accept": 0.681,
    "draft_mean_len": 3.6,
    "load_s": 50
   },
   "memory": [
    [
     "Gewichte (resident)",
     "52.1 GiB"
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
     "62.0 GiB"
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
     "38.4 GiB"
    ]
   ],
   "ctx_total": 163840,
   "ctx_per_slot": 163840,
   "slots": 1,
   "apt_mirror": "ftp.fau.de (131.188.12.211)"
  },
  "UD-IQ4_XS": {
   "log": "state/quality/tbmini-UD-IQ4_XS.log",
   "server_log": "state/logs/tbench-server-20260905-134327.log",
   "command": "ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-IQ4_XS/Qwen3.8-Flash-Next-UD-IQ4_XS-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{\"reasoning_effort\": \"medium\"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4",
   "server": {
    "requests": 294,
    "prompt_tokens": 339204,
    "generated_tokens": 343555,
    "pp_tps": 263.9,
    "tg_tps": 23.9,
    "draft_accept": 0.678,
    "draft_mean_len": 3.63,
    "load_s": 59
   },
   "memory": [
    [
     "Gewichte (resident)",
     "63.0 GiB"
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
     "72.9 GiB"
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
     "27.5 GiB"
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
  "UD-IQ1_M": {
   "file_gib": 69.4,
   "kld": 0.3147,
   "top1": 79.7,
   "footprint_gib": 55.1
  },
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
