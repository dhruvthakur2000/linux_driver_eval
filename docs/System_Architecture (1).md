# System Architecture

> Version: generated on 2025-07-29 19:47:13

This document describes the architecture of the **Linux Driver Code Evaluation Framework** as discovered from the uploaded project.

## High-Level Flow

```
prompts/*.txt  ──► code_runner.py ──► generated_code/*.c
                                    │
                                    ├──► evaluator.py
                                    │       ├─ compiler.py (GCC/WSL)
                                    │       ├─ evaluation/static_linter.py
                                    │       ├─ evaluation/functionality_checker.py
                                    │       ├─ evaluation/security_check.py
                                    │       ├─ evaluation/quality_check.py
                                    │       └─ metrics.py (weights + aggregation)
                                    │
                                    └──► reports/
                                            ├─ compilation_logs/*.log
                                            ├─ metrics/*.json
                                            └─ summaries/*.csv (via summary_generator.py)
```

## Modules Overview

- **main.py**  
  Entry point that delegates to `src/code_runner.py:main()` for code generation.

- **src/code_runner.py**  
  CLI tool to run a selected **Together** model on a given prompt file, extract code blocks, and save them to `generated_code/`.  
  Uses:
  - `src/models/model_registry.py` to map friendly names to actual model IDs.
  - `src/models/together.py` to call the Together API.
  - `src/utils.extract_code_blocks()` to strip markdown fences.
  - `src/utils.save_generated_code()` to persist outputs.

- **src/models/model_registry.py / src/models/together.py**  
  Encapsulate model selection and Together API calls.

- **src/compiler.py**  
  Compiles C files (syntax-only) and captures diagnostics. Supports **WSL bridging** by invoking `wsl gcc` and converting Windows paths to `/mnt/<drive>/...`. Produces timestamped logs under `logs/` and counts `warning:` / `error:` occurrences.

- **src/evaluator.py**  
  Orchestrates a full evaluation for one C file:
  - `compile_code()` from `compiler.py`
  - Static lint: `evaluation/static_linter.py`
  - Functional heuristics: `evaluation/functionality_checker.py`
  - Security heuristics: `evaluation/security_check.py`
  - Quality heuristics: `evaluation/quality_check.py`
  - Score aggregation: `metrics.score_all()`  
  Saves a JSON report to `reports/`.

- **src/evaluation/**  
  Modular checks returning metrics + findings:
  - `static_linter.py`: missing includes/functions/types; suspicious macros.
  - `functionality_checker.py`: presence of `struct file_operations`, required ops (open/read/write/release), simple error-handling/edge-case signals.
  - `security_check.py`: unsafe libc calls, user copy bounds signals, locks, and resource management.
  - `quality_check.py`: comment density, line-length, maintainability hints.
  - `static_analyzer.py`: a richer, consolidated analyzer (optional; parallel to finer-grained modules).

- **src/metrics.py**  
  Combines buckets into weighted scores (Correctness 40%, Security 25%, Code Quality 20%, Advanced/Performance 15%).

- **src/summary_generator.py**  
  Aggregates reports into summaries (CSV) for comparisons/leaderboards.

- **mock_linux_headers/**  
  Minimal stubs to allow syntax-checking kernel-like code without a full kernel tree.

- **tests/**  
  Contains `test_prompt_runner.py` for basic verification of the generation pipeline.

## Data & Artifacts

- **generated_code/**: model outputs (`*.c`)
- **logs/**: pipeline logs + compiler logs
- **reports/**:
  - `metrics/*.json` — per-file evaluation results
  - `compilation_logs/*.log` — raw compiler outputs
  - (optional) `summaries/*.csv` — generated rollups

## Environment & Execution Context

- **Together API**: `TOGETHER_API_KEY` is read from environment (see `.env`).
- **GCC/WSL**: On Windows, `src/compiler.py` can call `wsl gcc ...` and converts paths with `_to_wsl_path()`.
- **Logging**: `src/logger.py` writes to `logs/pipeline.log` with UTF‑8 file handler.

## Current Repository Tree (abridged)

```
.env
.gitignore
Final_test_summarization.py
README.md
docs/evaluation_rubric.md
docs/system_architecture.md
docs/user_guide.md
generated_code/char_driver.c
generated_code/deepseek_r1_20250729_182501.c
generated_code/deepseek_r1_20250729_182848.c
main.py
mock_header.py
mock_linux_headers/linux/cdev.h
mock_linux_headers/linux/device.h
mock_linux_headers/linux/fs.h
mock_linux_headers/linux/init.h
mock_linux_headers/linux/module.h
mock_linux_headers/linux/slab.h
mock_linux_headers/linux/types.h
mock_linux_headers/linux/uaccess.h
notebook/linux_driver_eval (1).ipynb
prompts/char_driver.txt
reports/char_driver_evaluation.json
reports/leaderboard.md
reports/summary/summary.csv
reports/summary.csv
requirements.txt
src/__init__.py
src/code_runner.py
src/compiler.py
src/errors.py
src/evaluation/adv_feature.py
src/evaluation/functionality_checker.py
src/evaluation/quality_check.py
src/evaluation/security_check.py
src/evaluation/static_analyzer.py
src/evaluation/static_linter.py
src/evaluator.py
src/logger.py
src/metrics.py
src/models/__init__.py
src/models/model_registry.py
src/models/together.py
src/summary_generator.py
src/utils.py
structure.py
tests/__init__.py
tests/test_prompt_runner.py
```