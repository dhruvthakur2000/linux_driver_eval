# Linux Driver Code Evaluation Framework

Evaluate and compare **LLM‑generated Linux character driver code** with fast, explainable, and reproducible metrics.

## ✨ Features

- **Code generation** via Together models (optional)
- **Syntax compilation** via GCC (with **WSL bridging** on Windows)
- **Static lint & heuristics** for functionality, security, and quality
- **Weighted scoring** (Correctness 40, Security 25, Quality 20, Advanced/Perf 15)
- **Logs & reports** for auditability

## 🚀 Quickstart

```bash
# (optional) set TOGETHER_API_KEY in .env
python main.py --prompt prompts/char_driver.txt --model qwen3_32b --output generated_code

# evaluate a C file
python -m src.evaluator --file generated_code/char_driver.c --output reports
```

## 📂 Project Structure (abridged)

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

## 🧠 Models

Configured in `src/models/model_registry.py`.
Detected keys: afm_preview, deepseek_distill, deepseek_r1, exaone_3_5, exaone_deep, llama3_turbo, llama_vision, qwen3_32b

## 🧪 Scoring

See `src/metrics.py` and **docs/Rubrics_and_Evaluation_Criteria.md** for weights and normalization.

## 🗂 Outputs

- `logs/` — pipeline + compiler logs
- `reports/metrics/*.json` — per‑file results
- `reports/summaries/*.csv` — rollups (via `summary_generator.py`)

## 🛠 Requirements

- Python 3.10+
- pip, venv
- GCC (or GCC in WSL)

## 📝 License

MIT (or project license as applicable).