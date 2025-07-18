from src.models.together import TogetherModel
from src.errors import ModelLoadError 
from src.logger import logger

together_models={
    "mistral": "mistralai/Mistral-7B-Instruct-v0.1",
    "phi": "microsoft/phi-2",
    "codegemma": "google/codegemma-7b-it",
    "starcoder": "bigcode/starcoder2-7b",
    "deepseek": "deepseek-ai/deepseek-coder-6.7b-instruct"
}

def get_model(model_key:str,api_key:str):
    if model_key not in together_models:
        logger.error(f" Unsupported model: {model_key}")
        raise ModelLoadError(f"Model '{model_key}' not supported ")
    logger.info(f" Model selected: {model_key}")
    return TogetherModel(together_models[model_key],api_key)
        