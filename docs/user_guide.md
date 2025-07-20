
# 📘 USER GUIDE

## 🔧 Project: LLM-Based Linux Driver Evaluation System

---

## 🗂️ Overview

This project evaluates how well large language models (LLMs) like Mistral, Phi, CodeGemma perform at generating Linux character device drivers. The system automatically:

- Prompts LLMs with predefined Linux driver tasks
- Saves generated code
- Evaluates the output for correctness
- Summarizes performance using metrics

---

## 📁 Folder Structure

```
linux_driver_eval/
├── prompts/                 # Prompt text files for each model
├── generated_code/          # Auto-generated C files from LLMs
├── reports/
│   ├── metrics/             # Individual JSON reports per model
│   └── summary/             # Summary CSV comparing models
├── src/
│   ├── models/              # LLM interface and model registry
│   ├── utils.py             # Code block extraction, saving
│   ├── evaluator.py         # Static evaluation logic
│   ├── summary.py           # CSV summary generation
│   ├── logger.py            # Custom logging
│   └── compiler.py          # [Optional] Static code checks (if used)
├── run_final_test.py        # ✅ Final script to run the full pipeline
├── user_guide.md            # 📘 You’re here!
└── requirements.txt         # Python dependencies
```

---

## ⚙️ Prerequisites

- Python 3.8+
- An active [Together AI](https://www.together.ai/) account with API key
- Installed requirements:  
  ```bash
  pip install -r requirements.txt
  ```

---

## 🔐 Environment Setup

1. Create a `.env` file in your project root:
    ```bash
    touch .env
    ```

2. Add your Together API key:
    ```
    TOGETHER_API_KEY=your_key_here
    ```

---

## 🚀 Running the Evaluation Pipeline

Use the main script:
```bash
python run_final_test.py
```

This will:
- Load each model and prompt
- Generate Linux driver code
- Evaluate code for quality and structure
- Save metrics in `reports/metrics/`
- Create a final summary in `reports/summary/summary.csv`

---

## 📊 Understanding the Results

Each model’s output is assessed on:

| Metric               | Description                                        |
|----------------------|----------------------------------------------------|
| `missing_functions`  | Key functions like `open`, `read`, `write`, etc.   |
| `missing_includes`   | Required kernel headers (`<linux/fs.h>`, etc.)     |
| `suspicious_macros`  | Usage of macros like `EFAULT`, `EIO`, etc.         |
| `function_score`     | Score out of 10 based on presence of core methods  |
| `optional_components`| Helpful extras like `file_operations`, `init` etc. |

View the final report at:  
`reports/summary/summary.csv`

---

## 🧪 Custom Testing

You can manually test code generation, compilation, or evaluation using:
```bash
python src/test_compile.py
```

---

## 🧰 Troubleshooting

- **Missing API key**: Ensure `.env` has a valid `TOGETHER_API_KEY`
- **Clang errors**: You may ignore compilation if only static evaluation is required
- **WSL issues**: Make sure your virtual environment is set up inside WSL

---

## 📦 To Submit

Include:
- This `user_guide.md`
- `reports/summary/summary.csv`
- Sample `.json` files in `reports/metrics/`
- A 3–5 minute screen recording demonstrating:
  - Code structure
  - Running the evaluation pipeline
  - Viewing the results
