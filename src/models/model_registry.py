from src.models.together import TogetherModel  


together_models = {
    "qwen3_32b": "Qwen/Qwen1.5-32B-Chat",
    "deepseek_r1": "deepseek-ai/DeepSeek-R1-0528",
    "afm_preview": "arcee/AFM-4.5B-Preview",
    "llama_vision": "meta-llama/Meta-Llama-Vision",
    "deepseek_distill": "deepseek-ai/DeepSeek-Coder-33B-Instruct",
    "exaone_deep": "lg-ai/EXAONE-32B",
    "exaone_3_5": "lg-ai/EXAONE-3.5-32B-Instruct",
    "llama3_turbo": "meta-llama/Meta-Llama-3-70B-Instruct"
}

def get_model(key: str):
    model_name = together_models.get(key)
    if model_name is None:
        raise ValueError(f"Model key '{key}' not found.")
    return TogetherModel(model_name)