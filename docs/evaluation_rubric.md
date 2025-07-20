# 📊 Evaluation Rubric

This rubric defines how each generated driver code is evaluated.

## ✅ Required Kernel Functions
| Function     | Points |
|--------------|--------|
| open         | 2.5    |
| read         | 2.5    |
| write        | 2.5    |
| release      | 2.5    |
| **Total**    | **10** |

## 📌 Required Includes (No points, but logged)
- `<linux/fs.h>`
- `<linux/init.h>`
- `<linux/module.h>`

## ⚠️ Suspicious Macros (Flagged)
- `EIO`
- `EFAULT`
- `copy_to_user`

## 🧩 Optional Checks
- Presence of `file_operations`
- Presence of `init/exit` module macros

## 🔍 Final Output
- JSON report with:
  - `missing_functions`
  - `missing_includes`
  - `suspicious_macros`
  - `function_score` (0-10)