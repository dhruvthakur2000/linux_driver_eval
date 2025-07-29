# User Guide — Running Evaluations

This guide explains how to generate code with an LLM, evaluate it, and view the results.

## 1) Prerequisites

- **Python 3.10+**
- **pip** and a virtual environment (recommended)
- **GCC**
  - Linux/macOS: install via system package manager
  - Windows: either install **MSYS2/MinGW-w64 GCC** or use **WSL** and let `compiler.py` call `wsl gcc ...`
- (Optional) Together API key in `.env` as `TOGETHER_API_KEY=...`

## 2) Setup

```bash
# from the repo root
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3) Generate Driver Code (optional)

If you want the pipeline to first generate code via Together models:

```bash
python main.py --prompt prompts/char_driver.txt --model qwen3_32b --output generated_code
```

This will:
- load the prompt from `prompts/...`
- call the selected model (see `src/models/model_registry.py`)
- extract fenced code blocks
- save a timestamped `generated_code/<model>_<timestamp>.c`

## 4) Evaluate a C File

Run the evaluator on any C file:

```bash
python -m src.evaluator --file generated_code/char_driver.c --output reports
```

What happens:
1. **Compilation** (syntax‑only) via `gcc` (WSL bridging supported)
2. **Static lint** — missing includes/functions/types
3. **Functionality** — file ops struct, required callbacks, error handling signals
4. **Security** — unsafe calls, user copy bounds, locks, resource mgmt
5. **Quality** — comments, long lines, maintainability
6. **Scoring** — weighted aggregation to 0–100

Outputs:
- `reports/metrics/<file>_<timestamp>.json` — structured metrics + scores
- `logs/*` — compiler logs + pipeline log

## 5) Viewing Summaries

Aggregate results (optional):

```bash
python -m src.summary_generator --input reports/metrics --output reports/summaries/summary.csv
```

## 6) Windows + WSL Notes

- If GCC is installed **in WSL**, `src/compiler.py` will run `wsl gcc` and convert Windows paths.  
- Ensure the project files live under a mounted drive (e.g., `C:\...` shows in WSL as `/mnt/c/...`).

## 7) Troubleshooting

- **gcc not found**: install GCC or ensure it’s on PATH; for WSL use `wsl gcc --version` from PowerShell.
- **API key errors**: ensure `.env` contains `TOGETHER_API_KEY` and you ran `pip install together`.
- **No code saved**: prompts must include a fenced block ```c ... ``` or plain C; we still fall back to raw text extraction.
- **Kernel headers missing**: the project uses `mock_linux_headers/`; for real builds you would point `-I` to kernel headers.