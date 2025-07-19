import re
import os
from src.logger import logger

def lint_c_code(file_path: str, report_path: str) -> dict:
    issues = {
        "missing_functions": [],
        "missing_types": [],
        "suspicious_macros": [],
        "missing_includes": []
    }
    
    try:
        with open(file_path, "r") as f:
            code = f.read()

        # Required function definitions
        for fn in ["open", "read", "write", "release"]:
            if not re.search(rf"\b{fn}\s*\(", code):
                issues["missing_functions"].append(fn)
    
        # Type usage checks
        for typ in ["ssize_t", "loff_t", "size_t"]:
            if typ not in code:
                issues["missing_types"].append(typ)

                # Kernel macros
        for macro in ["EIO", "EFAULT", "copy_to_user"]:
            if macro in code and f"#define {macro}" not in code:
                issues["suspicious_macros"].append(macro)

        # Include checks
        required_headers = [
            "<linux/init.h>", "<linux/module.h>", "<linux/fs.h>",
            "<linux/uaccess.h>", "<linux/cdev.h>"
        ]
        for header in required_headers:
            if header not in code:
                issues["missing_includes"].append(header)

        # Save report
        os.makedirs(report_path, exist_ok=True)
        report_file = os.path.join(report_path, f"{os.path.basename(file_path)}_lint.txt")
        with open(report_file, "w") as f:
            f.write(f"🔍 Static Lint Report for {file_path}\n\n")
            for k, v in issues.items():
                f.write(f"{k.replace('_', ' ').title()}:\n")
                if v:
                    for item in v:
                        f.write(f"  - {item}\n")
                else:
                    f.write("   None\n")
                f.write("\n")

        logger.info(f" Custom static lint report saved to {report_file}")
        return issues

    except Exception as e:
        logger.error(f" Static linting failed: {e}")
        return {}      