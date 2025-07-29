# Evaluation Rubrics & Scoring

This document explains the **metrics and heuristics** used to evaluate Linux driver code in this project.

## Buckets & Weights

Final scores are computed in `src/metrics.py` with the following weights:

- **Correctness** (40%) — compilation + functionality
- **Security** (25%)
- **Code Quality** (20%)
- **Advanced/Performance** (15%)

The output reports include a `scores` section with each bucket (0–100) and an `overall_score`.

## 1) Correctness

### 1.1 Compilation (from `src/compiler.py`)
- Toolchain: `gcc` (can run via WSL with `wsl gcc`)
- Flags: `-Wall -Wextra -fsyntax-only [-I mock_linux_headers]`
- Collected metrics:
  - `success` (return code == 0)
  - `warnings_count` (count of "warning:" in log)
  - `errors_count` (count of "error:" in log)
  - `log_file` (path to raw compiler output)

### 1.2 Functionality (from `evaluation/functionality_checker.py`)
Signals:
- Presence of `struct file_operations <id> = { ... }`
- Required callbacks: open, read, write, release
- Error handling hints:
  - use of `-EFAULT`, `-EINVAL`
  - bounds checks around user copies
  - cleanup with `goto` patterns
- Edge cases:
  - `min(...)`, `memmove(...)`
  - lock pairing `mutex_lock`/`mutex_unlock`

Each sub-metric is normalized to **0..1** and rounded to 2 decimals.

## 2) Security (from `evaluation/security_check.py`)

- **Buffer safety**: penalize `strcpy(`, `sprintf(`, `gets(`; reward bounds near user copies.
- **Race conditions**: reward presence of locks (`DEFINE_MUTEX`, `mutex_lock/unlock`), lightly penalize IRQ contexts without explicit locking signals.
- **Resource management**: ensure allocated memory (`kmalloc`/`kzalloc`) has a matching `kfree`.

## 3) Code Quality (from `evaluation/quality_check.py`)

- **Style compliance**: long-line warnings (> 140 chars) reduce score.
- **Documentation**: comment density ≥ 5% yields full credit.
- **Maintainability**: presence of `goto` slightly reduces score; extreme file length also penalized.

## 4) Static Lint (from `evaluation/static_linter.py`)

Checks detect missing:
- Functions: open, read, write, release
- Includes: <linux/fs.h>, <linux/init.h>, <linux/module.h>
- Types: ssize_t, loff_t, size_t
And suspicious macros: EIO, EFAULT, copy_to_user.

## 5) Advanced / Performance

- **Advanced** (flags only): device tree tables, power management (`suspend`/`resume`), debug facilities (`dev_dbg`, `debugfs`, `proc_create`).
- **Performance (light)**: simple heuristics around memory ops and buffer sizing (treated as part of the 15% bucket).

## Normalization & Aggregation

Each module returns `{ "metrics": {...}, "findings": {...} }` with values in **0..1**.  
`src/metrics.py` multiplies by weights, converts to 0–100, and computes `overall_score`.

## Limitations (and why acceptable)

- Regex heuristics can produce **false positives/negatives**.
- We don’t compile against a full kernel; instead we syntax‑check with **mock headers**.
- Despite limits, this design is **fast, deterministic, explainable**, and works well for **LLM output triage** before deep testing.