import os

PROJECT_ROOT = "."  # current dir

folders = [
    "prompts",
    "generated_code",
    "mock_linux_headers/linux",
    "reports",
    "src",
    "evaluation",
    "tests",
]

files = [
    "main.py",
    "README.md",
    "requirements.txt",
    "setup.py",
    "evaluation/__init__.py",
    "evaluation/compiler.py",
    "evaluation/metrics.py",
    "evaluation/static_analysis.py",
    "evaluation/rubric.py",
    "src/prompt_runner.py",
    "src/__init__.py",
    "tests/test_prompt_runner.py",
    "tests/__init__.py"
]

def create_structure():
    print(" Setting up your project structure...\n")
    for folder in folders:
        path = os.path.join(PROJECT_ROOT, folder)
        os.makedirs(path, exist_ok=True)
        print(f" Created folder: {path}")

    for file in files:
        file_path = os.path.join(PROJECT_ROOT, file)
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(file_path, "w") as f:
            f.write("")  # Empty file
        print(f" Created file: {file_path}")

    print("\n Project structure created successfully.")

if __name__ == "__main__":
    create_structure()
