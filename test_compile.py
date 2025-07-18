from src.compiler import compile_code

if __name__ == "__main__":
    model_name = "mistral"
    file_name = "char_driver.c"
    source_path = f"generated_code/{file_name}"

    success, output = compile_code(source_path, model_name)
    
    if success:
        print(" Compilation Succeeded.")
    else:
        print(" Compilation Failed.")
    
    print(" Compiler Output:\n", output)
