window.TBMINI = {
 "generated_at": "2026-09-04T10:52:53+00:00",
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
   "quant": "UD-Q4_K_XL",
   "inference_profile": "mtp4-ngram-thinking-medium",
   "engine": "llama.cpp",
   "engine_version": "0.3.0-dev (build 1, commit 60bce1a)",
   "backend": "rocm",
   "backend_version": "7.1.52802",
   "platform": "AMD Ryzen AI MAX+ 395 (Strix Halo)",
   "model": "Qwen3.8-Flash-Next",
   "n_ctx": 163840,
   "benchmark": null,
   "tb_version": null,
   "tb_revision": null,
   "harbor_version": null,
   "generated_at": "2026-09-04T10:40:29.441989+00:00",
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
     "attempts": 1
    }
   }
  }
 ],
 "commands": {
  "UD-Q2_K_XL": {
   "log": "state/quality/tbmini-UD-Q2_K_XL.log",
   "server_log": "state/logs/tbench-server-20260904-125044.log",
   "command": "ROCBLAS_USE_HIPBLASLT=1 /home/lyra/models/qwen38-flash/engine/build-engramhalo/bin/llama serve -m /home/lyra/.cache/huggingface/hub/models--unsloth--Qwen3.8-Flash-Next-GGUF/snapshots/824f539b2710e5a9e47af4952cf6578cf5ee8932/UD-Q2_K_XL/Qwen3.8-Flash-Next-UD-Q2_K_XL-00001-of-00003.gguf -ngl 99 -c 163840 -fa on -ctk q8_0 -ctv q8_0 -b 8192 -ub 2048 -t 4 --load-mode none -np 1 --cache-ram 2048 -md /home/lyra/.cache/huggingface/hub/models--dzannotti--Qwen3.8-Flash-Next-MTP-GGUF/snapshots/0b2551d191548168d3254ddea4ab943a5ef4f809/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf -ngld 99 --spec-type draft-mtp,ngram-mod --spec-draft-n-max 4 --spec-draft-p-min 0.75 --jinja --chat-template-kwargs '{\"reasoning_effort\": \"medium\"}' --temp 1 --top-p 0.95 --top-k 20 --min-p 0 --host 10.50.4.9 --port 8080 -a qwen3.8-flash --metrics -lv 4",
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
     "106.3 GiB"
    ],
    [
     "Reserve OS/Page-Cache",
     "6.0 GiB"
    ],
    [
     "Spielraum",
     "41.1 GiB"
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
