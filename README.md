# Linux Driver Code Evaluation Framework 🚀

This project evaluates the quality of Linux device driver code generated by LLMs like Mistral, Starcoder, CodeGemma, and others. It compiles the generated C code, performs static analysis, checks for required kernel-level functions and includes, and produces detailed reports.

## 📁 Directory Structure

```
├── prompts/                  # Prompt files for LLMs
├── generated_code/           # Output from LLMs (.c files)
├── reports/
│   ├── compilation_logs/     # Logs from clang compiler
│   ├── tidy_logs/            # Static analysis logs
│   └── metrics/              # Evaluation result JSONs
├── mock_linux_headers/       # Dummy headers to bypass kernel deps
├── src/
│   ├── compiler.py           # Compilation + static analysis
│   ├── evaluator.py          # Scoring based on rules
│   ├── logger.py             # File + terminal logging
│   └── models/               # LLM model interfaces
├── run_pipeline.py           # Main CLI entrypoint
├── requirements.txt
└── README.md
```

## ✅ Features

- Run Linux-driver prompts through LLMs via Together API
- Compile with `clang` using mock kernel headers
- Optional static analysis with `clang-tidy`
- Custom evaluation via regex + rubric scoring
- Generates metrics reports in JSON
- Supports multiple model evaluations

## 🔧 Setup

```bash
git clone https://github.com/yourname/linux-driver-evaluator.git
cd linux-driver-evaluator
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Usage

```bash
python run_pipeline.py --model mistral --prompt char_driver.txt
```

## 📊 Evaluation Output

The final evaluation report is stored as:
```
reports/metrics/char_driver_mistral.json
```

## 📚 Documentation

- [`user_guide.md`](user_guide.md) - How to run and evaluate
- [`system_architecture.md`](system_architecture.md) - Design and flow
- [`rubric.md`](rubric.md) - How evaluation metrics are scored

## 🧠 Models Supported

- mistral
- phi
- codegemma
- starcoder
- deepseek

## 👤 Author

Dhruv Thakur — [GitHub](https://github.com/dhruvthakur2000)